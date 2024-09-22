import pulp
import json

# Provided data in JSON format
data = {
    'buy_price': [
        [110, 120, 130, 110, 115],
        [130, 130, 110, 90, 115],
        [110, 140, 130, 100, 95],
        [120, 110, 120, 120, 125],
        [100, 120, 150, 110, 105],
        [90, 100, 140, 80, 135]
    ],
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
    'dependencies': [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}

# Extract data from the provided structure
I = len(data['buy_price'])  # Number of oil types
M = len(data['buy_price'][0])  # Number of months

# Create a problem variable
problem = pulp.LpProblem("Oil_Blend_Problem", pulp.LpMaximize)

# Decision Variables
buy_quantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['buy_price'][i][m] * buy_quantity[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M))

problem += profit

# Storage Dynamics
for i in range(I):
    for m in range(1, M):
        problem += storage[i][m] == storage[i][m-1] + buy_quantity[i][m] - refine[i][m]

for i in range(I):
    problem += storage[i][0] == data['init_amount']

# Storage Capacity
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= data['storage_size']

# Refining Capacity
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Final Product Hardness Condition
for m in range(M):
    problem += data['min_hardness'] <= pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / (pulp.lpSum(refine[i][m] for i in range(I)) + 1e-5)
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / (pulp.lpSum(refine[i][m] for i in range(I)) + 1e-5) <= data['max_hardness']

# Initial and Final Storage Constraint
for i in range(I):
    problem += storage[i][M-1] == data['init_amount']

# Usage Requirements and Dependencies
for i in range(I):
    for m in range(M):
        problem += refine[i][m] >= data['min_usage'] * (pulp.LpVariable(f'y_{i}_{m}', cat='Binary'))

for i in range(I):
    for j in range(I):
        problem += pulp.LpVariable(f'y_{j}') >= data['dependencies'][i][j] * pulp.LpVariable(f'y_{i}')

# Limitation on Oils per Month
for m in range(M):
    problem += pulp.lpSum(pulp.LpVariable(f'y_{i}_{m}') for i in range(I)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')