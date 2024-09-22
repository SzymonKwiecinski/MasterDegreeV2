import pulp

# Data from JSON
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

# Unpacking data
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
initial_amount = data['InitialAmount']

# Problem
problem = pulp.LpProblem("OilBlending", pulp.LpMaximize)

# Variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    sell_price * pulp.lpSum(refine[i, m] for i in range(I)) 
    - pulp.lpSum(buy_price[m][i] * buy_quantity[i, m] + storage_cost * storage[i, m] for i in range(I))
    for m in range(M)
)

# Constraints

# Initial Storage
for i in range(I):
    problem += (storage[i, 0] == initial_amount, f"InitialStorage_{i}")

# Storage Balance
for i in range(I):
    for m in range(M):
        problem += (storage[i, m + 1] == storage[i, m] + buy_quantity[i, m] - refine[i, m], f"StorageBalance_{i}_{m}")

# End Storage equal to Initial Amount
for i in range(I):
    problem += (storage[i, M] == initial_amount, f"EndStorage_{i}")

# Storage Capacity
for i in range(I):
    for m in range(M):
        problem += (storage[i, m] <= storage_size, f"StorageCapacity_{i}_{m}")

# Vegetable Oil Refining Capacity
for m in range(M):
    problem += (pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg, f"MaxVegRefining_{m}")

# Non-Vegetable Oil Refining Capacity
for m in range(M):
    problem += (pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg, f"MaxNonVegRefining_{m}")

# Hardness Constraints
for m in range(M):
    total_refined = pulp.lpSum(refine[i, m] for i in range(I))
    problem += (total_refined > 0) | (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refined >= min_hardness, f"MinHardness_{m}")
    problem += (total_refined > 0) | (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refined <= max_hardness, f"MaxHardness_{m}")

# Solve the problem
problem.solve()

# Print the output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')