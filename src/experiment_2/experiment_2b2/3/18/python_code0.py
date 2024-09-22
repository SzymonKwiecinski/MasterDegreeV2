import pulp

# Problem data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                 [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

# Constants
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)

# Objective function
revenue = pulp.lpSum(sell_price * pulp.lpSum(refine[i, m] for i in range(I) for m in range(M)))
costs = pulp.lpSum(buy_price[m][i] * buy[i, m] for i in range(I) for m in range(M))
storage_costs = pulp.lpSum(storage_cost * storage[i, m] for i in range(I) for m in range(1, M+1))
profit = revenue - costs - storage_costs
problem += profit

# Constraints
# Initial storage
for i in range(I):
    problem += storage[i, 0] == init_amount

# Balance equations
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] == storage[i, m-1] + buy[i, m-1] - refine[i, m-1]

# Storage capacity
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] <= storage_size

# Refining capacity
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

# Hardness requirement
for m in range(M):
    hardness_expr = pulp.lpSum((hardness[i] * refine[i, m]) for i in range(I))
    total_refined = pulp.lpSum(refine[i, m] for i in range(I))
    problem += hardness_expr >= min_hardness * total_refined
    problem += hardness_expr <= max_hardness * total_refined

# Final storage must be initial amount
for i in range(I):
    problem += storage[i, M] == init_amount

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buy": [[pulp.value(buy[i, m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i, m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i, m]) for i in range(I)] for m in range(M+1)]
}

# Print the output and objective value
print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')