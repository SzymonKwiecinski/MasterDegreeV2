import pulp

# Data
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

# Indices and parameters
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg_refining = data['MaxVegetableRefiningPerMonth']
max_non_veg_refining = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Problem definition
problem = pulp.LpProblem("MaximizeProfit", pulp.LpMaximize)

# Variables
buy = [[pulp.LpVariable(f'buy_{i}_{m}', lowBound=0) for i in range(I)] for m in range(M)]
refine = [[pulp.LpVariable(f'refine_{i}_{m}', lowBound=0) for i in range(I)] for m in range(M)]
storage = [[pulp.LpVariable(f'storage_{i}_{m}', lowBound=0) for i in range(I)] for m in range(M)]

# Objective function
profit = pulp.lpSum([
    sell_price * pulp.lpSum(refine[i][m] for i in range(I)) - 
    pulp.lpSum(buy_price[m][i] * buy[i][m] for i in range(I)) -
    pulp.lpSum(storage_cost * storage[i][m] for i in range(I))
    for m in range(M)
])
problem += profit

# Constraints

# Initial storage amount
for i in range(I):
    problem += storage[i][0] == init_amount + buy[i][0] - refine[i][0]

# Storage constraints and flow balance
for m in range(1, M):
    for i in range(I):
        problem += storage[i][m] == storage[i][m-1] + buy[i][m] - refine[i][m]
        problem += storage[i][m] <= storage_size

# Refining constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg_refining
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg_refining

# Hardness constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[i][m] for i in range(I))
    hardness_avg = pulp.lpSum(refine[i][m] * hardness[i] for i in range(I))
    if total_refine > 0:
        problem += hardness_avg / total_refine <= max_hardness
        problem += hardness_avg / total_refine >= min_hardness

# End storage must match initial amount
for i in range(I):
    problem += storage[i][M-1] == init_amount

# Solve the problem
problem.solve()

# Solution
solution = {
    "buy": [[pulp.value(buy[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')