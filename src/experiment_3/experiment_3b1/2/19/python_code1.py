import pulp
import json

# Load data
data = json.loads('''{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}''')

# Parameters
I = len(data['buy_price'])    # Number of oil types
M = len(data['buy_price'][0]) # Number of months
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
sell_price = data['sell_price']
storage_cost = data['storage_cost']
init_amount = data['init_amount']
min_usage = data['min_usage']
hardness = data['hardness']
dependencies = data['dependencies']

# Create the problem
problem = pulp.LpProblem("Oil Refining and Blending", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)

# Objective Function
profit = pulp.lpSum(sell_price * refine[i, m] for i in range(I) for m in range(M)) - \
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] + storage_cost * storage[i, m] for i in range(I) for m in range(M))
problem += profit

# Constraints
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]

    problem += storage[i, M-1] == init_amount  # Final month storage constraint

# Refining Limits
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= max_non_veg

# Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) >= data['min_hardness']
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) <= data['max_hardness']

# Usage Minimum
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= min_usage * (1 if pulp.lpSum(refine[j, m] for j in range(I) if refine[j, m] > 0) > 0 else 0)

# Dependency Constraints
for i in range(I):
    for m in range(M):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[j, m] >= min_usage * (1 if refine[i, m] > 0 else 0)

# Oil Selection Limit
for m in range(M):
    problem += pulp.lpSum(1 for i in range(I) if refine[i, m] > 0) <= 3

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')