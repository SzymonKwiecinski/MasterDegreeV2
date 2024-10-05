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

# Unpack data
I = data['I']
M = data['M']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable_refining_per_month = data['MaxVegetableRefiningPerMonth']
max_non_vegetable_refining_per_month = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
initial_amount = data['InitialAmount']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", [(i, m) for i in range(I) for m in range(M)], lowBound=0, cat='Continuous')
refine_quantity = pulp.LpVariable.dicts("RefineQuantity", [(i, m) for i in range(I) for m in range(M)], lowBound=0, cat='Continuous')
storage_quantity = pulp.LpVariable.dicts("StorageQuantity", [(i, m) for i in range(I) for m in range(M+1)], lowBound=0, cat='Continuous')

# Add initial storage amount
for i in range(I):
    problem += storage_quantity[i, 0] == initial_amount

# Constraints
for m in range(M):
    # Refining capacity constraints
    problem += pulp.lpSum(refine_quantity[i, m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month
    problem += pulp.lpSum(refine_quantity[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month
    
    # Storage constraints
    for i in range(I):
        problem += storage_quantity[i, m+1] == storage_quantity[i, m] + buy_quantity[i, m] - refine_quantity[i, m]
        problem += storage_quantity[i, m+1] <= storage_size
    
    # Hardness constraints
    total_refine = pulp.lpSum(refine_quantity[i, m] for i in range(I))
    problem += pulp.lpSum(hardness[i] * refine_quantity[i, m] for i in range(I)) >= min_hardness * total_refine
    problem += pulp.lpSum(hardness[i] * refine_quantity[i, m] for i in range(I)) <= max_hardness * total_refine

# Final storage must equal initial amount
for i in range(I):
    problem += storage_quantity[i, M] == initial_amount

# Objective
profit = pulp.lpSum(
    sell_price * pulp.lpSum(refine_quantity[i, m] for i in range(I)) 
    - pulp.lpSum(buy_price[m][i] * buy_quantity[i, m] for i in range(I))
    - storage_cost * pulp.lpSum(storage_quantity[i, m+1] for i in range(I))
    for m in range(M)
)
problem += profit

# Solve
problem.solve()

# Output
buy_solution = [[pulp.value(buy_quantity[i, m]) for i in range(I)] for m in range(M)]
refine_solution = [[pulp.value(refine_quantity[i, m]) for i in range(I)] for m in range(M)]
storage_solution = [[pulp.value(storage_quantity[i, m]) for i in range(I)] for m in range(M+1)]

output = {
    "buy": buy_solution,
    "refine": refine_solution,
    "storage": storage_solution
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')