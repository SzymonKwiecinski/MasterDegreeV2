import pulp

# Data from the JSON
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

# Parameters
I = len(data['buy_price'])
M = len(data['buy_price'][0])

# Problem
problem = pulp.LpProblem("Oil_Refinery_Profit_Maximization", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I+1) for m in range(M+1)), lowBound=0, upBound=data['storage_size'], cat='Continuous')
y = pulp.LpVariable.dicts("y", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective function
problem += pulp.lpSum([
    data['sell_price'] * pulp.lpSum(refine[i, m] for i in range(I)) -
    pulp.lpSum(buyquantity[i, m] * data['buy_price'][i][m] for i in range(I)) -
    pulp.lpSum(storage[i, m+1] * data['storage_cost'] for i in range(I))
    for m in range(M)
])

# Constraints
# Initial storage condition
for i in range(I):
    problem += storage[i, 0] == data['init_amount']

# Final storage condition
for i in range(I):
    problem += storage[i, M] == data['init_amount']

# Storage update
for i in range(I):
    for m in range(M):
        problem += storage[i, m+1] == storage[i, m] + buyquantity[i, m] - refine[i, m]

# Refining limits
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness constraints
for m in range(M):
    refine_sum = pulp.lpSum(refine[i, m] for i in range(I))
    if refine_sum > 0:
        problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * refine_sum
        problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * refine_sum

# Maximum three oils
for m in range(M):
    problem += pulp.lpSum(y[i, m] for i in range(I)) <= 3

# Minimum usage
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * y[i, m]

# Dependency constraints
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            for m in range(M):
                problem += y[i, m] <= y[j, m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')