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

# Initialize problem
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Variables
buy_quantity = pulp.LpVariable.dicts("buy_quantity", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([
    data['SellPrice'] * pulp.lpSum(refine[i, m] for i in range(data['I'])) -
    pulp.lpSum(data['BuyPrice'][m][i] * buy_quantity[i, m] for i in range(data['I'])) -
    pulp.lpSum(data['StorageCost'] * storage[i, m] for i in range(data['I']))
    for m in range(data['M'])
])
problem += profit

# Constraints
for m in range(data['M']):
    # Refining Capacity Constraints
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth']

    # Hardness Constraints
    total_refined = pulp.lpSum(refine[i, m] for i in range(data['I']))
    if total_refined > 0:
        weighted_hardness = pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / total_refined
        problem += weighted_hardness >= data['MinHardness']
        problem += weighted_hardness <= data['MaxHardness']

# Initial and final storage amounts
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount']
    problem += storage[i, data['M'] - 1] == data['InitialAmount']

# Storage balance constraints
for i in range(data['I']):
    for m in range(1, data['M']):
        problem += (
            storage[i, m] == storage[i, m - 1] + buy_quantity[i, m] - refine[i, m]
        )
        problem += storage[i, m] <= data['StorageSize']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')