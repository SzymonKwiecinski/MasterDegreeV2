import json
import pulp

# Input data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], 
                 [130, 130, 110, 90, 115], 
                 [110, 140, 130, 100, 95], 
                 [120, 110, 120, 120, 125], 
                 [100, 120, 150, 110, 105], 
                 [90, 100, 140, 80, 135]],
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

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variable definitions
M = data['M']
I = data['I']
buyquantity = pulp.LpVariable.dicts("BuyQuantity", (range(I), range(M)), 0)
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), 0)
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M)), 0)

# Objective function
profit = pulp.lpSum([(data['SellPrice'] * pulp.lpSum(refine[i][m] for i in range(I))) -
                      pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i][m] for i in range(I)))
                     for m in range(M)])

problem += profit

# Constraints

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], f"MaxVegetableRefining_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], f"MaxNonVegetableRefining_{m}"

# Storage capacity constraints
for m in range(M):
    for i in range(I):
        problem += storage[i][m] <= data['StorageSize'], f"StorageCapacity_{i}_{m}"

# Initial storage
for i in range(I):
    problem += storage[i][0] == data['InitialAmount'], f"InitialStorage_{i}"

# Storage balance constraints
for m in range(M-1):
    for i in range(I):
        problem += storage[i][m] + buyquantity[i][m] - refine[i][m] == storage[i][m+1], f"StorageBalance_{i}_{m}"

# Final storage must equal initial storage
for i in range(I):
    problem += storage[i][M-1] == data['InitialAmount'], f"FinalStorage_{i}"

# Hardness constraints
problem += pulp.lpSum(data['Hardness'][i] * pulp.lpSum(refine[i][m] for m in range(M)) for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) <= data['MaxHardness'], "MaxHardness"
problem += pulp.lpSum(data['Hardness'][i] * pulp.lpSum(refine[i][m] for m in range(M)) for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) >= data['MinHardness'], "MinHardness"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

# Print results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')