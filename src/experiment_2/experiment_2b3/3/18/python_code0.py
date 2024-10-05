import pulp

# Data from JSON
data = {'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}

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

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Oil_Refinery", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)

# Objective Function
profit_expr = pulp.lpSum([
    (sell_price - buy_price[m][i]) * refine[i, m] - storage_cost * storage[i, m+1]
    for i in range(I) for m in range(M)
])
problem += profit_expr

# Constraints
for i in range(I):
    problem += storage[i, 0] == init_amount

for m in range(M):
    veg_total = pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i])
    non_veg_total = pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i])

    problem += veg_total <= max_veg
    problem += non_veg_total <= max_non_veg

    for i in range(I):
        problem += storage[i, m+1] == storage[i, m] + buy[i, m] - refine[i, m]
        problem += storage[i, m+1] <= storage_size

    hardness_constraint = pulp.lpSum([
        hardness[i] * refine[i, m] for i in range(I)
    ])
    total_refined = pulp.lpSum(refine[i, m] for i in range(I))

    problem += hardness_constraint <= max_hardness * total_refined
    problem += hardness_constraint >= min_hardness * total_refined

for i in range(I):
    problem += storage[i, M] == init_amount

# Solve the problem
problem.solve()

# Prepare the Output
buy_quantity_output = [[pulp.value(buy[i, m]) for i in range(I)] for m in range(M)]
refine_quantity_output = [[pulp.value(refine[i, m]) for i in range(I)] for m in range(M)]
storage_output = [[pulp.value(storage[i, m]) for i in range(I)] for m in range(M+1)]

output = {
    "buy": buy_quantity_output,
    "refine": refine_quantity_output,
    "storage": storage_output
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')