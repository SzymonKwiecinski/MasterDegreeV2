import pulp

# Data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [0, 1, 1, 1, 1],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300],
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Sets
K = len(data['profit'])  # Number of products
M = len(data['num_machines'])  # Number of machines
I = len(data['limit'][0])  # Number of months

# Decision Variables
sell = pulp.LpVariable.dicts('sell', ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts('manufacture', ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts('storage', ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts('maintain', ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
profit_terms = [data['profit'][k] * sell[k, i] for k in range(K) for i in range(I)]
storage_cost_terms = [data['store_price'] * storage[k, i] for k in range(K) for i in range(I)]
problem += pulp.lpSum(profit_terms) - pulp.lpSum(storage_cost_terms)

# Constraints
# 1. Production time availability:
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K)) <= data['n_workhours'] * 12 * (24 - sum(min(i, data['down'][m]) for m in range(M)))

# 2. Marketing limitations:
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= data['limit'][k][i]

# 3. Storage constraints:
for k in range(K):
    for i in range(I):
        problem += storage[k, i] <= 100

# 4. Stock requirements:
for k in range(K):
    for i in range(I):
        problem += storage[k, i] + manufacture[k, i] - sell[k, i] == data['keep_quantity']

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')