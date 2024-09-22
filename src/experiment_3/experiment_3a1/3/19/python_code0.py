import pulp
import json

# Load data
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Parameters
M = len(data['buy_price'][0])  # Number of months
I = len(data['buy_price'])       # Number of oils
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

# Define problem
problem = pulp.LpProblem("Oil Refining Problem", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size)

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I)) for m in range(M)) - \
                   pulp.lpSum(buy_price[i][m] * buyquantity[i][m] for i in range(I) for m in range(M)) - \
                   storage_cost * pulp.lpSum(storage[i][m] for i in range(I) for m in range(M))
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

for i in range(I):
    for m in range(M):
        problem += storage[i][m] == (storage[i][m-1] + buyquantity[i][m] - refine[i][m]) if m > 0 else init_amount

for i in range(I):
    for m in range(M):
        problem += storage[i][m] >= 0
        problem += storage[i][m] <= storage_size

for i in range(I):
    problem += storage[i][0] == init_amount
    problem += storage[i][M-1] == init_amount

for m in range(M):
    problem += min_hardness <= (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I))) <= max_hardness

for i in range(I):
    for m in range(M):
        problem += refine[i][m] >= min_usage * (refine[i][m] > 0)

for i in range(I):
    for j in range(I):
        if dependencies[i][j] == 1:
            for m in range(M):
                problem += refine[j][m] <= refine[i][m]

for m in range(M):
    problem += pulp.lpSum(refine[i][m] > 0 for i in range(I)) <= 3

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')