import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity",
                                    ((i, m) for i in range(data['I']) for m in range(data['M'])),
                                    lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine",
                               ((i, m) for i in range(data['I']) for m in range(data['M'])),
                               lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage",
                                ((i, m) for i in range(data['I']) for m in range(data['M']+1)),
                                lowBound=0, cat='Continuous')

# Objective
profit = (
    pulp.lpSum([
        data['SellPrice'] * refine[(i, m)] -
        data['BuyPrice'][m][i] * buyquantity[(i, m)] -
        data['StorageCost'] * storage[(i, m+1)]
        for i in range(data['I']) for m in range(data['M'])
    ])
)
problem += profit, "Total Profit"

# Constraints
# Initial storage condition
for i in range(data['I']):
    problem += storage[(i, 0)] == data['InitialAmount']

# Storage dynamics
for i in range(data['I']):
    for m in range(1, data['M']+1):
        problem += storage[(i, m)] == storage[(i, m-1)] + buyquantity[(i, m-1)] - refine[(i, m-1)]

# Final storage condition
for i in range(data['I']):
    problem += storage[(i, data['M'])] == data['InitialAmount']

# Refining capacity constraints
for m in range(data['M']):
    problem += pulp.lpSum([refine[(i, m)] for i in range(data['I']) if data['IsVegetable'][i]]) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum([refine[(i, m)] for i in range(data['I']) if not data['IsVegetable'][i]]) <= data['MaxNonVegetableRefiningPerMonth']

# Storage constraints
for i in range(data['I']):
    for m in range(1, data['M']+1):
        problem += storage[(i, m)] <= data['StorageSize']

# Hardness constraints
for m in range(data['M']):
    hardness_expression = pulp.lpSum([data['Hardness'][i] * refine[(i, m)] for i in range(data['I'])])
    total_refine = pulp.lpSum([refine[(i, m)] for i in range(data['I'])])
    
    problem += hardness_expression >= data['MinHardness'] * total_refine
    problem += hardness_expression <= data['MaxHardness'] * total_refine

# Solve the problem
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')