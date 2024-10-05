import pulp

# Data Input
data = {
    'buy_price': [[110, 120, 130, 110, 115], 
                  [130, 130, 110, 90, 115], 
                  [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], 
                  [100, 120, 150, 110, 105], 
                  [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

# Initialize problem
problem = pulp.LpProblem("Oil_Refining_Profit_Maximization", pulp.LpMaximize)

# Sets
I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("Use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['sell_price'] * pulp.lpSum(refine[i, m] for i in range(I)) -
    pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] + data['storage_cost'] * storage[i, m] 
               for i in range(I))
    for m in range(M)
)

# Constraints

# Storage Constraints
for i in range(I):
    for m in range(1, M):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m]
    problem += storage[i, 0] == data['init_amount'] + buyquantity[i, 0] - refine[i, 0]
    problem += storage[i, M-1] == data['init_amount']

# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness Constraints
for m in range(M):
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += total_refine * data['min_hardness'] <= pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= total_refine * data['max_hardness']

# Minimum Usage Constraints
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * x[i, m]

# Dependency Constraints
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j]:
            for m in range(M):
                problem += refine[j, m] <= M * x[i, m]

# Usage Limitation Constraint
for m in range(M):
    problem += pulp.lpSum(x[i, m] for i in range(I)) <= 3

# Storage Limit Constraints
for i in range(I):
    for m in range(M):
        problem += storage[i, m] <= data['storage_size']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')