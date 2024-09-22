import pulp
import json

data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

I = len(data['buy_price'])
M = len(data['buy_price'][0])
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
is_vegetable = data['is_vegetable']
dependencies = data['dependencies']
hardness = data['hardness']

# Create the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M + 1)), lowBound=0, upBound=storage_size, cat='Continuous')
y = pulp.LpVariable.dicts("y", (range(I), range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum([sell_price * pulp.lpSum([refine[i][m] for i in range(I)]) - 
                        pulp.lpSum([data['buy_price'][i][m] * buyquantity[i][m] + storage_cost * storage[i][m] for i in range(I)]) 
                        for m in range(M)])

# Initial and Final Storage Constraints
for i in range(I):
    problem += storage[i][0] == init_amount
    problem += storage[i][M] == init_amount

# Material Balance
for i in range(I):
    for m in range(M):
        problem += storage[i][m + 1] == storage[i][m] + buyquantity[i][m] - refine[i][m]

# Storage Capacity Constraint
for i in range(I):
    for m in range(M + 1):
        problem += storage[i][m] >= 0
        problem += storage[i][m] <= storage_size

# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum([refine[i][m] for i in range(I) if is_vegetable[i]]) <= max_veg
    problem += pulp.lpSum([refine[i][m] for i in range(I) if not is_vegetable[i]]) <= max_non_veg

# Hardness Constraint
for m in range(M):
    problem += min_hardness <= pulp.lpSum([hardness[i] * refine[i][m] for i in range(I)]) / \
                  pulp.lpSum([refine[i][m] for i in range(I)]) <= max_hardness

# Oil Usage Limit
for m in range(M):
    for i in range(I):
        problem += refine[i][m] >= min_usage * y[i][m]
    problem += pulp.lpSum([y[i][m] for i in range(I)]) <= 3

# Dependency Constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            problem += y[i][m] >= dependencies[i][j] * y[j][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')