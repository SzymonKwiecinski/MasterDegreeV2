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

# Indices
months = range(data['M'])
oils = range(data['I'])

# Problem
problem = pulp.LpProblem("Oil_Refinement", pulp.LpMaximize)

# Variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", (oils, months), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (oils, months), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (oils, months), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['SellPrice'] * pulp.lpSum(refine[i][m] for i in oils) - 
                      pulp.lpSum(data['BuyPrice'][m][i] * buy_quantity[i][m] + 
                                 data['StorageCost'] * storage[i][m] for i in oils)
                      for m in months)

# Constraints
for i in oils:
    problem += (storage[i][0] == data['InitialAmount'], f'Initial Storage {i}')
    problem += (storage[i][data['M'] - 1] == data['InitialAmount'], f'Final Storage {i}')

    for m in months:
        if m > 0:
            problem += (storage[i][m] == storage[i][m-1] + buy_quantity[i][m] - refine[i][m], f'Storage Balance {i}_{m}')
        problem += (storage[i][m] <= data['StorageSize'], f'Storage Limit {i}_{m}')

# Refining Capacity Constraints
for m in months:
    problem += (pulp.lpSum(refine[i][m] for i in oils if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], f'Vegetable Refining {m}')
    problem += (pulp.lpSum(refine[i][m] for i in oils if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], f'Non-Vegetable Refining {m}')

# Hardness Constraints
for m in months:
    total_refine = pulp.lpSum(refine[i][m] for i in oils)
    if total_refine > 0:
        hardness = pulp.lpSum(data['Hardness'][i] * refine[i][m] for i in oils) / total_refine
        problem += (hardness >= data['MinHardness'], f'Min Hardness {m}')
        problem += (hardness <= data['MaxHardness'], f'Max Hardness {m}')

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')