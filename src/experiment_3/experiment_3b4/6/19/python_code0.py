import pulp

# Data
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

# Problem
problem = pulp.LpProblem("OilBlending", pulp.LpMaximize)

# Sets
I = len(data['is_vegetable'])
M = len(data['buy_price'][0])

# Decision Variables
buyquantity = pulp.LpVariable.dicts('buyquantity', ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat=pulp.LpContinuous)
refine = pulp.LpVariable.dicts('refine', ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat=pulp.LpContinuous)
storage = pulp.LpVariable.dicts('storage', ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat=pulp.LpContinuous)
use = pulp.LpVariable.dicts('use', ((i, m) for i in range(I) for m in range(M)), cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum([
    data['sell_price'] * refine[i, m] - data['buy_price'][i][m] * buyquantity[i, m] - data['storage_cost'] * storage[i, m]
    for i in range(I) for m in range(M)
])

# Constraints
# Initial storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']

# Storage balance
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1]

# Final storage requirement
for i in range(I):
    problem += storage[i, M] == data['init_amount']

# Storage capacity limit
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] <= data['storage_size']

# Vegetable oil refining capacity
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']

# Non-vegetable oil refining capacity
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness requirement
for m in range(M):
    refine_sum = pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * refine_sum
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * refine_sum

# Usage restrictions
for m in range(M):
    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

# Minimum usage if used
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

# Dependency constraints
for i in range(I):
    for j in range(I):
        for m in range(M):
            if data['dependencies'][i][j]:
                problem += use[i, m] >= use[j, m]

# Solve
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')