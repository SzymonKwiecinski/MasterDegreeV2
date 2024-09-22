import pulp

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

# Define the LP problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Define variables
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("Y", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective function
profit = pulp.lpSum([
    data['sell_price'] * pulp.lpSum(refine[i, m] for i in range(I)) -
    pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I)) -
    data['storage_cost'] * pulp.lpSum(storage[i, m] for i in range(I))
    for m in range(M)
])

problem += profit

# Constraints

# 1. Balance Constraints
for i in range(I):
    for m in range(M):
        problem += storage[i, m+1] == storage[i, m] + buyquantity[i, m] - refine[i, m]

# 2. Initial and Final Storage Constraints
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M] == data['init_amount']

# 3. Refining Capacity
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# 4. Storage Capacity
for i in range(I):
    for m in range(M+1):
        problem += storage[i, m] <= data['storage_size']

# 5. Hardness Constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * total_refine
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * total_refine

# 6. Limited Oils in Blend
for m in range(M):
    problem += pulp.lpSum(y[i, m] for i in range(I)) <= 3

# 7. Minimum Usage
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * y[i, m]

# 8. Dependencies
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            for m in range(M):
                problem += y[i, m] <= y[j, m]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')