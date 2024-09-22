import pulp

# Data
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

I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months

# Variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Objective
revenue = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M))
costs = pulp.lpSum(data['buy_price'][i][m] * buy_quantity[i, m] for i in range(I) for m in range(M))
storage_costs = pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M))
problem += revenue - costs - storage_costs

# Constraints
for m in range(M):
    # Flow balance
    for i in range(I):
        if m == 0:
            problem += storage[i, m] == data['init_amount'] + buy_quantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buy_quantity[i, m] - refine[i, m]

    # Refining capacity
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    # Hardness constraints
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += total_refine >= 0  # Ensure total_refine is non-negative first
    hardness_expr = pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I))
    problem += hardness_expr >= data['min_hardness'] * total_refine
    problem += hardness_expr <= data['max_hardness'] * total_refine

    # Usage constraints
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

    # Dependency constraints
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j]:
                problem += use[i, m] <= use[j, m] + 1 - data['dependencies'][i][j]

# Storage limits
for i in range(I):
    for m in range(M+1):
        problem += storage[i, m] <= data['storage_size']

# Initial and end storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M] == data['init_amount']

# Solve
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')