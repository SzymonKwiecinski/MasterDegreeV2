import json
import pulp

# Input data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], 
                 [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], 
                 [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
total_revenue = pulp.lpSum(refine[i][m] * sell_price for i in range(I) for m in range(M))
total_cost = pulp.lpSum(buyquantity[i][m] * buy_price[m][i] for i in range(I) for m in range(M)) + \
              pulp.lpSum(storage[i][m] * storage_cost for i in range(I) for m in range(M))
problem += total_revenue - total_cost

# Constraints
for m in range(M):
    for i in range(I):
        if is_vegetable[i]:
            problem += pulp.lpSum(refine[i][m] for m in range(M) if m == month) <= max_veg, f"MaxVegetableRefining_{m}_{i}"
        else:
            problem += pulp.lpSum(refine[i][m] for m in range(M) if m == month) <= max_non_veg, f"MaxNonVegetableRefining_{m}_{i}"

# Storage constraints
for i in range(I):
    problem += storage[i][0] == init_amount, f"InitialStorage_{i}"

for m in range(1, M):
    for i in range(I):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"StorageBalance_{i}_{m}"

# Final storage condition
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"FinalStorageCondition_{i}"

# Hardness constraints
problem += pulp.lpSum(hardness[i] * refine[i][m] for i in range(I) for m in range(M)) / \
           pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) <= max_hardness, "MaxHardness"
problem += pulp.lpSum(hardness[i] * refine[i][m] for i in range(I) for m in range(M)) / \
           pulp.lpSum(refine[i][m] for i in range(I) for m in range(M)) >= min_hardness, "MinHardness"

# Solve the problem
problem.solve()

# Prepare results
buy_results = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_results = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_results = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

# Output results
output = {
    "buy": buy_results,
    "refine": refine_results,
    "storage": storage_results
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')