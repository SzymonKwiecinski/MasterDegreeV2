import pulp

data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'SellPrice': 150,
    'IsVegetable': [True, True, False, False, False],
    'MaxVegetableRefiningPerMonth': 200,
    'MaxNonVegetableRefiningPerMonth': 250,
    'StorageSize': 1000,
    'StorageCost': 5,
    'MinHardness': 3,
    'MaxHardness': 6,
    'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'InitialAmount': 500
}

M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg = data['MaxVegetableRefiningPerMonth']
max_non_veg = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("Buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')

# Initial amount constraint
for i in range(I):
    problem += storage[i, 0] == init_amount

# Storage constraints and refining constraints
for m in range(M):
    for i in range(I):
        problem += storage[i, m+1] == storage[i, m] + buy[i, m] - refine[i, m]
        problem += storage[i, m+1] <= storage_size

    # Refining limits
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

    # Hardness constraint
    hardness_expression = pulp.lpSum(refine[i, m] * hardness[i] for i in range(I))
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += hardness_expression >= min_hardness * total_refine
    problem += hardness_expression <= max_hardness * total_refine

# Final storage constraint
for i in range(I):
    problem += storage[i, M] == init_amount

# Objective function
profit = pulp.lpSum((sell_price - buy_price[m][i]) * refine[i, m] - storage_cost * storage[i, m+1] for i in range(I) for m in range(M))
problem += profit

# Solve the problem
problem.solve()

output = {
    "buy": [[pulp.value(buy[i, m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i, m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i, m]) for i in range(I)] for m in range(M + 1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>') 