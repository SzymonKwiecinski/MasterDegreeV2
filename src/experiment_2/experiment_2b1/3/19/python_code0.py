import pulp
import json

# Input data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Problem setup
I = len(data['buy_price'][0])  # Number of oils
M = len(data['buy_price'])      # Number of months

# Create the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
total_profit = pulp.lpSum([
    (data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I))) -
    pulp.lpSum(data['buy_price'][m][i] * buyquantity[i][m] for i in range(I))
    for m in range(M)
])
problem += total_profit

# Constraints

# Storage initialization
for i in range(I):
    problem += storage[i][0] == data['init_amount'], f"InitialStorage_{i}"

# Buy and Storage Constraints
for m in range(M):
    for i in range(I):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"StorageBalance_{i}_{m}"

# Storage limit
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= data['storage_size'], f"MaxStorage_{i}_{m}"

# Refining limits
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"MaxVegRefine_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"MaxNonVegRefine_{m}"

# Hardness Constraints
for m in range(M):
    problem += (pulp.lpSum(data['hardness'][i] * (refine[i][m] / pulp.lpSum(refine[j][m] for j in range(I) if refine[j][m] > 0)) for i in range(I) if refine[i][m] > 0) >= data['min_hardness']), f"MinHardness_{m}"
    problem += (pulp.lpSum(data['hardness'][i] * (refine[i][m] / pulp.lpSum(refine[j][m] for j in range(I) if refine[j][m] > 0)) for i in range(I) if refine[i][m] > 0) <= data['max_hardness']), f"MaxHardness_{m}"

# Dependencies Constraints
for m in range(M):
    for i in range(I):
        if data['dependencies'][i].count(1) > 0:
            problem += refine[i][m] <= pulp.lpSum(refine[j][m] for j in range(I) if data['dependencies'][i][j] == 1) * 1000, f"Dependency_{i}_{m}"

# Minimum usage constraints
for m in range(M):
    for i in range(I):
        problem += (refine[i][m] >= data['min_usage'] * pulp.lpSum([1 for j in range(I) if refine[j][m] > 0]), f"MinUsage_{i}_{m}")

# Final storage constraint
for i in range(I):
    problem += storage[i][M-1] == data['init_amount'], f"FinalStorage_{i}"

# Solve the problem
problem.solve()

# Output results
buy_result = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_result = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_result = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

result = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')