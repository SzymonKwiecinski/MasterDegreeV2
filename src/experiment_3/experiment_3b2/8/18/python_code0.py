import pulp
import json

# Data from JSON
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

# Set up the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(data['I']), range(data['M'])), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(data['I']), range(data['M'])), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(data['I']), range(data['M'])), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['SellPrice'] * pulp.lpSum(refine[i][m] for i in range(data['I'])) for m in range(data['M']))
cost = pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i][m] for i in range(data['I']) for m in range(data['M']))
storage_cost = pulp.lpSum(data['StorageCost'] * storage[i][m] for i in range(data['I']) for m in range(data['M']))
problem += profit - cost - storage_cost, "Total_Profit"

# Constraints

# Hardness Constraints
for m in range(data['M']):
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i][m] for i in range(data['I'])) / 
                 pulp.lpSum(refine[i][m] for i in range(data['I']))) >= data['MinHardness'], f"Min_Hardness_{m}"
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i][m] for i in range(data['I'])) / 
                 pulp.lpSum(refine[i][m] for i in range(data['I']))) <= data['MaxHardness'], f"Max_Hardness_{m}"

# Production capacity constraints
for m in range(data['M']):
    problem += (pulp.lpSum(refine[i][m] for i in range(data['I']) if data['IsVegetable'][i]) <= 
                 data['MaxVegetableRefiningPerMonth'], f"MaxVegRefining_{m}")
    problem += (pulp.lpSum(refine[i][m] for i in range(data['I']) if not data['IsVegetable'][i]) <= 
                 data['MaxNonVegetableRefiningPerMonth'], f"MaxNonVegRefining_{m}")

# Storage capacity constraints
for i in range(data['I']):
    for m in range(data['M']):
        problem += storage[i][m] <= data['StorageSize'], f"Storage_Capacity_{i}_{m}"

# Material balance constraints
for i in range(data['I']):
    for m in range(1, data['M']):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"Material_Balance_{i}_{m}"

# Initial storage constraints
for i in range(data['I']):
    problem += storage[i][0] == data['InitialAmount'], f"Initial_Storage_{i}"

# End period storage requirement
for i in range(data['I']):
    problem += storage[i][data['M'] - 1] == data['InitialAmount'], f"End_Storage_{i}"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')