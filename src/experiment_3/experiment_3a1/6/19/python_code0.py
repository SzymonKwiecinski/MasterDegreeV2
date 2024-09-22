import pulp
import json

# Input data
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Parameters
I = len(data['buy_price'])  # Number of raw oils
M = len(data['buy_price'][0])  # Number of months
buy_price = data['buy_price']
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
max_vegetable_refining_per_month = data['max_vegetable_refining_per_month']
max_non_vegetable_refining_per_month = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']

# Create the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), 0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), 0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), 0, storage_size)

# Objective Function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i, m] for i in range(I)) for m in range(M)) - \
               pulp.lpSum(buy_price[i][m] * buyquantity[i, m] + storage_cost * storage[i, m] for i in range(I) for m in range(M)), "Total_Profit"

# Constraints

# Storage balance
for m in range(1, M):
    for i in range(I):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m]

# Initial storage
for i in range(I):
    problem += storage[i, 0] == init_amount

# Final storage equals initial amount
for i in range(I):
    problem += storage[i, M] == init_amount

# Storage capacity
for m in range(M):
    for i in range(I):
        problem += storage[i, m] <= storage_size

# Maximum refining constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month

# Hardness constraints
for m in range(M):
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) >= min_hardness
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) <= max_hardness

# Usage constraints
for m in range(M):
    for i in range(I):
        problem += refine[i, m] >= min_usage * pulp.LpVariable(f'y_{i}_{m}', cat='Binary')

# Dependency constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[j, m] <= M * pulp.LpVariable(f'y_{i}_{m}', cat='Binary')

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')