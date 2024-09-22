import pulp
import json

# Load the data from the provided JSON format
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

# Define parameters based on the data
I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months
price = data['buy_price']
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
max_hardness = data['max_hardness']
min_hardness = data['min_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependency = data['dependencies']

# Create the optimization problem
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)
use = pulp.LpVariable.dicts("use", (range(I), range(M)), cat=pulp.LpBinary)

# Objective function
problem += pulp.lpSum([sell_price * pulp.lpSum([refine[i][m] for i in range(I)]) - 
                        pulp.lpSum([(price[i][m] * buyquantity[i][m] + storage_cost * storage[i][m])
                                     for i in range(I)])
                        for m in range(M)])

# Constraints
# Storage balance
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i][m] == init_amount + buyquantity[i][m] - refine[i][m]
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]

# Storage limits
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= storage_size

# Refining capacity
for m in range(M):
    problem += pulp.lpSum([refine[i][m] for i in range(I) if is_vegetable[i]]) <= max_veg
    problem += pulp.lpSum([refine[i][m] for i in range(I) if not is_vegetable[i]]) <= max_non_veg

# Hardness requirement
for m in range(M):
    problem += pulp.lpSum([(hardness[i] * refine[i][m] / pulp.lpSum([refine[j][m] for j in range(I)]) if pulp.lpSum([refine[j][m] for j in range(I)]) > 0 else 1)
                            for i in range(I)]) <= max_hardness
    problem += pulp.lpSum([(hardness[i] * refine[i][m] / pulp.lpSum([refine[j][m] for j in range(I)]) if pulp.lpSum([refine[j][m] for j in range(I)]) > 0 else 1)
                            for i in range(I)]) >= min_hardness

# Oil usage
for m in range(M):
    problem += pulp.lpSum([use[i][m] for i in range(I)]) <= 3
    for i in range(I):
        problem += refine[i][m] >= min_usage * use[i][m]
        for j in range(I):
            problem += use[i][m] >= dependency[i][j] * use[j][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')