import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)

# Objective Function
profit = pulp.lpSum([
    data['SellPrice'] * pulp.lpSum(refine[i, m] for i in range(data['I']))
    - pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i, m] for i in range(data['I']))
    - pulp.lpSum(data['StorageCost'] * storage[i, m] for i in range(data['I']))
    for m in range(data['M'])
])
problem += profit

# Constraints
for i in range(data['I']):
    # Initial storage
    problem += storage[i, 0] == data['InitialAmount'] + buyquantity[i, 0] - refine[i, 0]
    # Storage balance and end condition
    for m in range(1, data['M']):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
        problem += storage[i, m] <= data['StorageSize']
    # End storage condition
    problem += storage[i, data['M']-1] == data['InitialAmount']

# Refining capacity
for m in range(data['M']):
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth']

# Hardness constraints
for m in range(data['M']):
    total_refine_m = pulp.lpSum(refine[i, m] for i in range(data['I']))
    total_hardness_m = pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I']))
    problem += total_hardness_m >= data['MinHardness'] * total_refine_m
    problem += total_hardness_m <= data['MaxHardness'] * total_refine_m

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')