import pulp
import json

# Data from the JSON format
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

# Model parameters
I = len(data['buy_price'])  # number of oil types
M = len(data['buy_price'][0])  # number of months

# Create the LP problem
problem = pulp.LpProblem("OilRefiningBlending", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['sell_price'] * sum(refine[i][m] for i in range(I)) for m in range(M)) \
           - pulp.lpSum(sum(data['buy_price'][i][m] * buyquantity[i][m] for i in range(I)) for m in range(M)) \
           - pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M))

# Constraints
# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage Constraints
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= data['storage_size']
    problem += storage[i][M-1] == data['init_amount']

# Hardness Constraints
for m in range(M):
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                (pulp.lpSum(refine[i][m] for i in range(I)) + 1e-5) >= data['min_hardness'])
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                (pulp.lpSum(refine[i][m] for i in range(I)) + 1e-5) <= data['max_hardness'])

# Oil Usage Constraints
for m in range(M):
    for i in range(I):
        problem += refine[i][m] >= data['min_usage'] * pulp.LpVariable(f'x_{i}_{m}', 0, 1)
    problem += pulp.lpSum(pulp.LpVariable(f'x_{i}_{m}', 0, 1) for i in range(I)) <= 3

# Dependency Constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[j][m] >= data['min_usage'] * pulp.LpVariable(f'x_{i}_{m}', 0, 1)

# Storage Dynamics
for m in range(M-1):
    for i in range(I):
        problem += storage[i][m+1] == storage[i][m] + buyquantity[i][m] - refine[i][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')