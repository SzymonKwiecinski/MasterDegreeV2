import pulp
import json

# Data input
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Parameters
buy_price = data['buy_price']
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

# Set indices
I = range(len(buy_price))  # Set of oils
M = range(len(buy_price[0]))  # Set of months

# Create the problem
problem = pulp.LpProblem("Oil_Blending_and_Refining", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (I, M), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (I, M), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (I, M), lowBound=0, upBound=storage_size, cat='Continuous')
delta = pulp.LpVariable.dicts("delta", (I, M), cat='Binary')

# Objective Function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in I) - 
                       (pulp.lpSum(buy_price[i][m] * buyquantity[i][m] for i in I) + 
                        storage_cost * pulp.lpSum(storage[i][m] for i in I)) 
                       for m in M)

# Refining constraints
for m in M:
    problem += pulp.lpSum(refine[i][m] for i in I if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i][m] for i in I if not is_vegetable[i]) <= max_non_veg

# Storage constraints
for m in M:
    for i in I:
        if m == 0:
            problem += storage[i][m] == init_amount + buyquantity[i][m] - refine[i][m]
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]
        problem += storage[i][m] <= storage_size

# Initial and final storage
for i in I:
    problem += storage[i][0] == init_amount
    problem += storage[i][len(M)-1] == init_amount

# Hardness constraint
for m in M:
    problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in I) / 
                 pulp.lpSum(refine[i][m] for i in I)) <= max_hardness
    problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in I) / 
                 pulp.lpSum(refine[i][m] for i in I)) >= min_hardness

# Usage constraints
for m in M:
    for i in I:
        problem += refine[i][m] >= min_usage * delta[i][m]

# Dependency constraints
for m in M:
    for i in I:
        for j in I:
            problem += refine[j][m] >= dependencies[i][j] * delta[i][m] * refine[i][m]

# Manufacturing constraints
for m in M:
    problem += pulp.lpSum(delta[i][m] for i in I) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')