import pulp

# Data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
problem = pulp.LpProblem("Oil_Refining_Optimization", pulp.LpMaximize)

# Variables
buy_quantity = pulp.LpVariable.dicts("buyquantity",
                                     [(i, m) for i in range(data['I']) for m in range(data['M'])],
                                     lowBound=0, cat='Continuous')

refine = pulp.LpVariable.dicts("refine",
                               [(i, m) for i in range(data['I']) for m in range(data['M'])],
                               lowBound=0, cat='Continuous')

storage = pulp.LpVariable.dicts("storage",
                                [(i, m) for i in range(data['I']) for m in range(data['M'] + 1)],
                                lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([
    data['SellPrice'] * pulp.lpSum(refine[i, m] for i in range(data['I'])) -
    pulp.lpSum(data['BuyPrice'][m][i] * buy_quantity[i, m] for i in range(data['I'])) -
    data['StorageCost'] * pulp.lpSum(storage[i, m + 1] for i in range(data['I']))
    for m in range(data['M'])
]), "Total_Profit"

# Constraints

# Initial storage condition
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount'], f"Initial_Storage_{i}"

# Storage constraints
for i in range(data['I']):
    for m in range(1, data['M'] + 1):
        problem += storage[i, m] == storage[i, m - 1] + buy_quantity[i, m - 1] - refine[i, m - 1], f"Storage_Flow_{i}_{m}"
        problem += storage[i, m] <= data['StorageSize'], f"Max_Storage_{i}_{m}"

# Refining constraints
for m in range(data['M']):
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], f"Max_Vegetable_Refining_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], f"Max_Non_Vegetable_Refining_{m}"

# Hardness constraints
for m in range(data['M']):
    total_refined = pulp.lpSum(refine[i, m] for i in range(data['I']))
    problem += pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) >= data['MinHardness'] * total_refined, f"Min_Hardness_{m}"
    problem += pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) <= data['MaxHardness'] * total_refined, f"Max_Hardness_{m}"

# Final storage condition
for i in range(data['I']):
    problem += storage[i, data['M']] == data['InitialAmount'], f"Final_Storage_{i}"

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')