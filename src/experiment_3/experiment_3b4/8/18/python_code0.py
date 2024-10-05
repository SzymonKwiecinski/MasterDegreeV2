import pulp

# Data from JSON
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

# Initialize the problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", [(i, m) for i in range(data['I']) for m in range(data['M'])], lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", [(i, m) for i in range(data['I']) for m in range(data['M'])], lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", [(i, m) for i in range(data['I']) for m in range(data['M'])], lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    data['SellPrice'] * pulp.lpSum(refine[i, m] for i in range(data['I'])) -
    pulp.lpSum(data['BuyPrice'][m][i] * buy[i, m] for i in range(data['I'])) -
    data['StorageCost'] * pulp.lpSum(storage[i, m] for i in range(data['I']))
    for m in range(data['M'])
)

# Constraints

# Refining capacity constraints
for m in range(data['M']):
    problem += pulp.lpSum(data['IsVegetable'][i] * refine[i, m] for i in range(data['I'])) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum((1 - data['IsVegetable'][i]) * refine[i, m] for i in range(data['I'])) <= data['MaxNonVegetableRefiningPerMonth']

# Storage capacity constraint
for i in range(data['I']):
    for m in range(data['M']):
        problem += storage[i, m] <= data['StorageSize']

# Material balance constraints
for i in range(data['I']):
    for m in range(data['M']):
        if m == 0:
            problem += storage[i, m] == data['InitialAmount'] + buy[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buy[i, m] - refine[i, m]

# Final storage requirement
for i in range(data['I']):
    problem += storage[i, data['M']-1] == data['InitialAmount']

# Hardness constraint
for m in range(data['M']):
    problem += (
        data['MinHardness'] * pulp.lpSum(refine[i, m] for i in range(data['I'])) <=
        pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I']))
    )
    problem += (
        pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) <=
        data['MaxHardness'] * pulp.lpSum(refine[i, m] for i in range(data['I']))
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')