import pulp
import json

# Data from the provided JSON
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
problem = pulp.LpProblem("OilRefining", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", (range(data['I']), range(data['M'])), 0)
refine = pulp.LpVariable.dicts("Refine", (range(data['I']), range(data['M'])), 0)
storage = pulp.LpVariable.dicts("Storage", (range(data['I']), range(data['M'])), 0)

# Objective function
profit = pulp.lpSum(data['SellPrice'] * refine[i][m] for i in range(data['I']) for m in range(data['M'])) \
         - pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i][m] for i in range(data['I']) for m in range(data['M'])) \
         - pulp.lpSum(data['StorageCost'] * storage[i][m] for i in range(data['I']) for m in range(data['M']))

problem += profit

# Refining capacity constraints
for m in range(data['M']):
    problem += pulp.lpSum(refine[i][m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum(refine[i][m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth']

# Storage constraints
for i in range(data['I']):
    for m in range(data['M']):
        problem += storage[i][m] <= data['StorageSize']
        problem += storage[i][m] >= 0

# Hardness constraint and storage dynamics
for m in range(1, data['M']):
    problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m] for i in range(data['I'])

# Initial amounts
for i in range(data['I']):
    problem += storage[i][0] == data['InitialAmount']

# Final storage requirement
for i in range(data['I']):
    problem += storage[i][data['M']-1] == data['InitialAmount']

# Hardness constraint
for m in range(data['M']):
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i][m] for i in range(data['I'])) / 
                pulp.lpSum(refine[i][m] for i in range(data['I']))) >= data['MinHardness']
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i][m] for i in range(data['I'])) / 
                pulp.lpSum(refine[i][m] for i in range(data['I']))) <= data['MaxHardness']

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')