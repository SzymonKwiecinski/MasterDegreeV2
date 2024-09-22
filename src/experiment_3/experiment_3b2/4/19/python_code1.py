import pulp
import json

# Data in JSON format
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0, 5.5],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
}

# Define the problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Indices
I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months

# Decision Variables
buy = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (range(I), range(M)), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['buy_price'][i][m] * buy[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M))

problem += profit

# Constraints
# Storage Balance
for i in range(I):
    for m in range(1, M):
        problem += storage[i][m-1] + buy[i][m] - refine[i][m] == storage[i][m]

# Initial Storage
for i in range(I):
    problem += storage[i][0] == data['init_amount']

# End Storage
for i in range(I):
    problem += storage[i][M-1] == data['init_amount']

# Vegetable and Non-Vegetable Refining Capacity
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness Constraint
for m in range(M):
    problem += (
        (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I))) 
        >= data['min_hardness']
    )
    problem += (
        (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I))) 
        <= data['max_hardness']
    )

# Storage Capacity
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= data['storage_size']

# Usage at least min_usage
for i in range(I):
    for m in range(M):
        problem += refine[i][m] >= data['min_usage'] * y[i][m]

# Oil Usage Dependency
for i in range(I):
    for j in range(I):
        if i != j:
            for m in range(M):
                problem += y[i][m] <= y[j][m] + (1 - data['dependencies'][i][j])

# Max 3 Oils Used per Month
for m in range(M):
    problem += pulp.lpSum(y[i][m] for i in range(I)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')