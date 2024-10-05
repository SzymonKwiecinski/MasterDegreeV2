import pulp
import json

# Data input
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Initialize the problem
I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months

problem = pulp.LpProblem("Oil_Manufacturing_Problem", pulp.LpMaximize)

# Decision Variables
buy = pulp.LpVariable.dicts("buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
use = pulp.LpVariable.dicts("use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['buy_price'][i][m] * buy[i, m] + data['storage_cost'] * storage[i, m-1] for i in range(I) for m in range(1, M))
problem += profit

# Constraints

# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(data['is_vegetable'][i] * refine[i, m] for i in range(I)) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum((1 - data['is_vegetable'][i]) * refine[i, m] for i in range(I)) <= data['max_non_vegetable_refining_per_month']

# Storage Constraints
for i in range(I):
    problem += storage[i, 0] == data['init_amount']  # Initial storage
    problem += storage[i, M-1] == data['init_amount']  # Storage at the end of the last month
    for m in range(1, M):
        problem += storage[i, m] == storage[i, m-1] + buy[i, m] - refine[i, m]
        problem += storage[i, m] >= 0
        problem += storage[i, m] <= data['storage_size']

# Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * pulp.lpSum(refine[i, m] for i in range(I))

# Usage Constraints
for m in range(M):
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]
    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

# Dependency Constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += use[i, m] <= use[j, m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')