import pulp

# Data from the JSON
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

# Create a Linear Programming problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", 
                                    ((i, m) for i in range(data['I']) for m in range(data['M'])), 
                                    lowBound=0, cat='Continuous')

refine = pulp.LpVariable.dicts("refine", 
                               ((i, m) for i in range(data['I']) for m in range(data['M'])), 
                               lowBound=0, cat='Continuous')

storage = pulp.LpVariable.dicts("storage", 
                                ((i, m) for i in range(data['I']) for m in range(data['M'] + 1)), 
                                lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(
    data['SellPrice'] * pulp.lpSum(refine[i, m] for i in range(data['I'])) -
    pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i, m] + data['StorageCost'] * storage[i, m] for i in range(data['I']))
    for m in range(data['M'])
)

problem += profit

# Constraints

# Initial storage
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount']

# Refining capacity constraints
for m in range(data['M']):
    problem += pulp.lpSum(refine[i, m] * data['IsVegetable'][i] for i in range(data['I'])) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum(refine[i, m] * (1 - data['IsVegetable'][i]) for i in range(data['I'])) <= data['MaxNonVegetableRefiningPerMonth']

# Storage constraints
for i in range(data['I']):
    for m in range(data['M']):
        problem += storage[i, m] <= data['StorageSize']
    problem += storage[i, data['M']] == data['InitialAmount']

# Hardness constraints
for m in range(data['M']):
    total_refine = pulp.lpSum(refine[i, m] for i in range(data['I']))
    problem += pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) >= data['MinHardness'] * total_refine
    problem += pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) <= data['MaxHardness'] * total_refine

# Balance constraints
for i in range(data['I']):
    for m in range(1, data['M'] + 1):
        problem += storage[i, m - 1] + buyquantity[i, m - 1] == refine[i, m - 1] + storage[i, m]

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')