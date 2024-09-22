import pulp
import json

# Load data from JSON format
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Define the problem
I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']
is_vegetable = data['is_vegetable']

problem = pulp.LpProblem("OilProduction", pulp.LpMaximize)

# Create decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective Function
profit = pulp.lpSum(sell_price * refine[i, m] for i in range(I) for m in range(M)) - \
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I) for m in range(M)) - \
         storage_cost * pulp.lpSum(storage[i, m] for i in range(I) for m in range(M))

problem += profit

# Storage constraint
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m]

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

# Hardness constraint
for m in range(M):
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += total_refine > 0  # To avoid division by zero
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refine >= min_hardness
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refine <= max_hardness

# Final month's storage constraint
for i in range(I):
    problem += storage[i, M-1] == init_amount

# Usage dependency constraint
for m in range(M):
    for i in range(I):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[i, m] <= refine[j, m]  # If i is used, j must be used

# Minimum usage constraint
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= min_usage * pulp.lpSum(1 if refine[i, m] > 0 else 0 for m in range(M))

# Oil usage constraint
for m in range(M):
    problem += pulp.lpSum(1 for i in range(I) if refine[i, m] > 0) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')