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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)
M = data['M']
I = data['I']

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, upBound=data['StorageSize'])

# Objective Function
problem += pulp.lpSum([
    data['SellPrice'] * pulp.lpSum([refine[(i, m)] for i in range(I)]) -
    pulp.lpSum([data['BuyPrice'][m][i] * buyquantity[(i, m)] + data['StorageCost'] * storage[(i, m)] for i in range(I)])
    for m in range(M)
])

# Constraints
for i in range(I):
    for m in range(M):
        problem += storage[(i, m)] == (data['InitialAmount'] if m == 0 else storage[(i, m-1)]) + buyquantity[(i, m)] - refine[(i, m)]

for i in range(I):
    problem += storage[(i, M)] == data['InitialAmount']

for m in range(M):
    problem += pulp.lpSum(refine[(i, m)] for i in range(I) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum(refine[(i, m)] for i in range(I) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth']

for m in range(M):
    total_refine = pulp.lpSum(refine[(i, m)] for i in range(I))
    if total_refine > 0:
        problem += pulp.lpSum(data['Hardness'][i] * refine[(i, m)] for i in range(I)) >= data['MinHardness'] * total_refine
        problem += pulp.lpSum(data['Hardness'][i] * refine[(i, m)] for i in range(I)) <= data['MaxHardness'] * total_refine

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')