import pulp
import json

# Input Data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Extracting data
I = len(data['buy_price'][0])  # Number of oils
M = len(data['buy_price'])       # Number of months
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
init_amount = data['init_amount']
min_usage = data['min_usage']
hardness = data['hardness']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i, m] for i in range(I) for m in range(M))
       - pulp.lpSum(data['buy_price'][m][i] * buyquantity[i, m] for i in range(I) for m in range(M)) 
       - pulp.lpSum(storage_size * data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M)))

# Constraints
for m in range(M):
    # Refining capacity constraints
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= max_veg, f"MaxVegRefiningMonth{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= max_non_veg, f"MaxNonVegRefiningMonth{m}"
    
    # Storage update constraints
    for i in range(I):
        if m == 0:
            problem += storage[i, m] == init_amount, f"InitialStorageOil{i}"
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m], f"StorageUpdateOil{i}Month{m}"
        problem += storage[i, m] <= storage_size, f"MaxStorageOil{i}Month{m}"
    
    # Minimum usage constraints
    for i in range(I):
        if data['dependencies'][i].count(1) > 0:
            problem += refine[i, m] >= min_usage * sum(data['dependencies'][i]), f"MinUsageOil{i}Month{m}"

# Hardness constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += (total_refine > 0, f"TotalRefinePositiveMonth{m}")  # Ensure total refine is positive before division
    problem += (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refine >= min_hardness), f"MinHardnessMonth{m}"
    problem += (pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refine <= max_hardness), f"MaxHardnessMonth{m}"

# Last month storage constraint
for i in range(I):
    problem += storage[i, M-1] == init_amount, f"FinalStorageOil{i}"

# Solve the problem
problem.solve()

# Output result
buy = [[pulp.value(buyquantity[i, m]) for i in range(I)] for m in range(M)]
refine_out = [[pulp.value(refine[i, m]) for i in range(I)] for m in range(M)]
storage_out = [[pulp.value(storage[i, m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy,
    "refine": refine_out,
    "storage": storage_out
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')