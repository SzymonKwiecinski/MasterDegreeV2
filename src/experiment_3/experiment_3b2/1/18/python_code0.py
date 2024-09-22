import pulp
import json

# Data provided in JSON format
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

# Model Creation
problem = pulp.LpProblem("Oil Refinement and Blending", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((m, i) for m in range(1, data['M'] + 1) 
                                                        for i in range(data['I'])), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((m, i) for m in range(1, data['M'] + 1) 
                                            for i in range(data['I'])), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((m, i) for m in range(data['M'] + 1) 
                                              for i in range(data['I'])), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['SellPrice'] * refine[m, i] for m in range(1, data['M'] + 1) 
                       for i in range(data['I'])) \
           - pulp.lpSum(data['BuyPrice'][m-1][i] * buyquantity[m, i] for m in range(1, data['M'] + 1) 
                        for i in range(data['I'])) \
           - data['StorageCost'] * pulp.lpSum(storage[m, i] for m in range(1, data['M'] + 1) 
                                                for i in range(data['I']))

# Initial Storage Constraints
for i in range(data['I']):
    problem += storage[0, i] == data['InitialAmount']

# Storage Balance Constraints
for m in range(1, data['M'] + 1):
    for i in range(data['I']):
        problem += storage[m, i] == storage[m-1, i] + buyquantity[m, i] - refine[m, i]

# Final Storage Constraints
for i in range(data['I']):
    problem += storage[data['M'], i] == data['InitialAmount']

# Refining Capacity Constraints
for m in range(1, data['M'] + 1):
    problem += pulp.lpSum(refine[m, i] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum(refine[m, i] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth']

# Hardness Constraints
for m in range(1, data['M'] + 1):
    problem += pulp.lpSum(data['Hardness'][i] * refine[m, i] for i in range(data['I'])) \
                >= data['MinHardness'] * pulp.lpSum(refine[m, i] for i in range(data['I']))
    problem += pulp.lpSum(data['Hardness'][i] * refine[m, i] for i in range(data['I'])) \
                <= data['MaxHardness'] * pulp.lpSum(refine[m, i] for i in range(data['I']))

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')