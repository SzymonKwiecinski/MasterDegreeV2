import pulp

# Data received in JSON format
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

# Extracting data
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg = data['MaxVegetableRefiningPerMonth']
max_non_veg = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(M + 1) for i in range(I)), lowBound=0, cat='Continuous')

# Objective: Maximize Profit
profit = pulp.lpSum(
    (sell_price * pulp.lpSum(refine[m, i] for i in range(I)) -
     pulp.lpSum(buy_price[m][i] * buy[m, i] for i in range(I)) -
     storage_cost * pulp.lpSum(storage[m + 1, i] for i in range(I)))
    for m in range(M)
)
problem += profit

# Constraints
for i in range(I):
    # Initial storage
    problem += (storage[0, i] == init_amount)

# Storage balance constraints
for m in range(M):
    for i in range(I):
        problem += (storage[m + 1, i] == storage[m, i] + buy[m, i] - refine[m, i])

# Refining capacity constraints
for m in range(M):
    problem += (pulp.lpSum(refine[m, i] for i in range(I) if is_vegetable[i]) <= max_veg)
    problem += (pulp.lpSum(refine[m, i] for i in range(I) if not is_vegetable[i]) <= max_non_veg)

# Hardness constraints
for m in range(M):
    total_refined = pulp.lpSum(refine[m, i] for i in range(I))
    if total_refined > 0:
        hardness_calc = pulp.lpSum(hardness[i] * refine[m, i] for i in range(I)) / total_refined
        problem += (hardness_calc >= min_hardness)
        problem += (hardness_calc <= max_hardness)

# Storage capacity constraints
for m in range(1, M + 1):
    for i in range(I):
        problem += (storage[m, i] <= storage_size)

# Ending storage constraints
for i in range(I):
    problem += (storage[M, i] == init_amount)

# Solve the problem
problem.solve()

# Preparing Output
output = {
    "buy": [[pulp.value(buy[m, i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m, i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m, i]) for i in range(I)] for m in range(M + 1)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')