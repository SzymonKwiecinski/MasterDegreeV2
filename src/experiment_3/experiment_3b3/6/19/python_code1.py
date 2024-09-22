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

# Indices
I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months

# Decision variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("Y", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective function
problem += pulp.lpSum([
    data['sell_price'] * pulp.lpSum(refine[i, m] for i in range(I)) -
    pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I)) -
    pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I))
    for m in range(M)
])

# Constraints
# Initial storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']

# Storage balance
for i in range(I):
    for m in range(1, M):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]

# Final storage condition
for i in range(I):
    problem += storage[i, M-1] == data['init_amount']

# Capacity limitations
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness restrictions
for m in range(M):
    total_refine_m = pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * total_refine_m
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * total_refine_m

# Oil usage constraints
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * y[i, m]

# Dependency constraints
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            for m in range(M):
                problem += refine[j, m] >= data['min_usage'] * y[j, m]

# At most three oils constraint
for m in range(M):
    problem += pulp.lpSum(y[i, m] for i in range(I)) <= 3

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')