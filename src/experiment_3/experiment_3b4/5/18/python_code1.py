import pulp

# Data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [
        [110, 120, 130, 110, 115], 
        [130, 130, 110, 90, 115], 
        [110, 140, 130, 100, 95], 
        [120, 110, 120, 120, 125], 
        [100, 120, 150, 110, 105], 
        [90, 100, 140, 80, 135]
    ],
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
problem = pulp.LpProblem("Oil_Refining", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(data['I']) for m in range(data['M'] + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    data['SellPrice'] * refine[i, m] 
    - data['BuyPrice'][m][i] * buyquantity[i, m]
    - data['StorageCost'] * storage[i, m]
    for i in range(data['I']) for m in range(data['M'])
)

# Initial Storage Constraint
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount']

# Final Storage Constraint
for i in range(data['I']):
    problem += storage[i, data['M']] == data['InitialAmount']

# Balance Constraints
for i in range(data['I']):
    for m in range(data['M']):
        problem += storage[i, m + 1] == storage[i, m] + buyquantity[i, m] - refine[i, m]

# Storage Capacity Constraints
for i in range(data['I']):
    for m in range(data['M']):
        problem += storage[i, m] <= data['StorageSize']

# Vegetable Refining Capacity Constraints
for m in range(data['M']):
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth']

# Non-Vegetable Refining Capacity Constraints
for m in range(data['M']):
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth']

# Hardness Constraints
for m in range(data['M']):
    refined_sum = pulp.lpSum(refine[i, m] for i in range(data['I']))
    problem += refined_sum > 0  # This ensures we only apply the hardness constraints when refining is happening
    problem += pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / refined_sum >= data['MinHardness']
    problem += pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / refined_sum <= data['MaxHardness']

# Solve
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')