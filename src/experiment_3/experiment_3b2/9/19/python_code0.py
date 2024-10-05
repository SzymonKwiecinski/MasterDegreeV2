import pulp
import json

# Load data from JSON
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Parameters
I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
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

# Create the problem
problem = pulp.LpProblem("Optimal_Buying_Storage_Manufacturing", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
y = pulp.LpVariable.dicts("y", ((i, m) for i in range(I) for m in range(M)), cat="Binary")

# Objective Function
problem += pulp.lpSum(sell_price * refine[i, m] for i in range(I) for m in range(M)) - \
           pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I) for m in range(M)) - \
           pulp.lpSum(storage_cost * storage[i, m] for i in range(I) for m in range(M))

# Constraints
# (1) Storage balance
for i in range(I):
    problem += storage[i, 0] == init_amount  # Initial storage
    for m in range(1, M):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
    problem += storage[i, M-1] == init_amount  # Final storage

# (2) Refinement capacity
for m in range(M):
    problem += pulp.lpSum(is_vegetable[i] * refine[i, m] for i in range(I)) <= max_veg
    problem += pulp.lpSum((1 - is_vegetable[i]) * refine[i, m] for i in range(I)) <= max_non_veg

# (3) Storage capacity
for i in range(I):
    for m in range(M):
        problem += storage[i, m] <= storage_size

# (4) Hardness constraints
for m in range(M):
    problem += min_hardness * pulp.lpSum(refine[i, m] for i in range(I)) <= \
               pulp.lpSum(hardness[i] * refine[i, m] for i in range(I))
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) <= \
               max_hardness * pulp.lpSum(refine[i, m] for i in range(I))

# (5) Oil usage limitation
for m in range(M):
    problem += pulp.lpSum(y[i, m] for i in range(I)) <= 3
    for i in range(I):
        problem += refine[i, m] >= min_usage * y[i, m]

# (6) Dependency constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            problem += y[i, m] <= y[j, m] + (1 - dependencies[i][j])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')