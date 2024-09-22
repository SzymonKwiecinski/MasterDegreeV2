import pulp
import json

# Data input
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Parameters
I = len(data['buy_price'])
M = len(data['buy_price'][0])
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

# Initialize the problem
problem = pulp.LpProblem("Oil Refining and Blending", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
y = pulp.LpVariable.dicts("y", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i, m] for i in range(I)) - 
                    pulp.lpSum(buy_price[i][m] * buyquantity[i, m] for i in range(I)) - 
                    pulp.lpSum(storage_cost * storage[i, m] for i in range(I)) 
                    for m in range(M))

problem += profit

# Constraints

# Refining Limits
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month

# Storage Limits
for i in range(I):
    for m in range(M):
        problem += storage[i, m] <= storage_size

# Hardness Constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += min_hardness <= pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / (total_refine + 1e-5)
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / (total_refine + 1e-5) <= max_hardness

# Initial Storage Constraints
for i in range(I):
    problem += storage[i, 0] == init_amount

# Final Storage Constraints
for i in range(I):
    problem += storage[i, M-1] == init_amount

# Monthly Storage Dynamics
for i in range(I):
    for m in range(M - 1):
        problem += storage[i, m + 1] == storage[i, m] + buyquantity[i, m] - refine[i, m]

# Usage Constraints
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= min_usage * y[i, m]

# Dependency Constraints
for i in range(I):
    for m in range(M):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[i, m] <= 1000 * y[j, m]  # Big M method

# Oil Type Limit
for m in range(M):
    problem += pulp.lpSum(y[i, m] for i in range(I)) <= 3

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')