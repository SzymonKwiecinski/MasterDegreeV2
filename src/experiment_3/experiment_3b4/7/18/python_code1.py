import pulp

# Data
data = {
    'M': 6, 'I': 5, 
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

# Constants
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable_refining = data['MaxVegetableRefiningPerMonth']
max_nonvegetable_refining = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
initial_amount = data['InitialAmount']

# Problem
problem = pulp.LpProblem("RefineryOptimization", pulp.LpMaximize)

# Decision Variables
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([
    sell_price * pulp.lpSum(refine[i, m] for i in range(I)) 
    - pulp.lpSum(buy_price[m][i] * buy_quantity[i, m] for i in range(I))
    - storage_cost * pulp.lpSum(storage[i, m] for i in range(I))
    for m in range(M)
])

problem += profit

# Constraints
for i in range(I):
    problem += (storage[i, 0] == initial_amount)  # Initial storage

    for m in range(M):
        # Storage balance
        problem += (storage[i, m] + buy_quantity[i, m] == refine[i, m] + storage[i, m+1])
        # Storage capacity
        problem += (storage[i, m] <= storage_size)

    # Final storage back to initial amount
    problem += (storage[i, M] == initial_amount)

for m in range(M):
    # Vegetable refining capacity
    problem += (pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining)

    # Non-vegetable refining capacity
    problem += (pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_nonvegetable_refining)

    # Hardness constraints
    total_refined = pulp.lpSum(refine[i, m] for i in range(I))
    problem += (total_refined >= 0)  # Ensure total refined is non-negative
    average_hardness = pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refined
    problem += (average_hardness >= min_hardness)
    problem += (average_hardness <= max_hardness)

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')