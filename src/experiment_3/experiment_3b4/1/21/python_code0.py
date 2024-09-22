import pulp

# Data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05],
        [0.0, 0.0, 0.0, 0.2, 0.01]
    ],
    'down': [0, 1, 1, 1, 1],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

K = len(data['profit'])     # Number of products
I = len(data['limit'][0])   # Number of months
M = len(data['num_machines'])  # Number of machine types

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("Maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in range(K) for i in range(I))

# Constraints

# Manufacturing and Sales Constraints
for k in range(K):
    problem += (storage[k, 0] == 0)
    for i in range(I):
        if i == 0:
            problem += (manufacture[k, i] == sell[k, i] + 0 - storage[k, i])
        else:
            problem += (manufacture[k, i] == sell[k, i] + storage[k, i - 1] - storage[k, i])

# Machine Time Constraints
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(manufacture[k, i] * data['time'][k][m] for k in range(K)) <= 
                    (data['num_machines'][m] - maintain[m, i]) * 24 * 2 * data['n_workhours'])

# Maintenance Constraints
for m in range(M):
    problem += (pulp.lpSum(maintain[m, i] for i in range(I)) == data['down'][m])

# Marketing Limitation Constraints
for k in range(K):
    for i in range(I):
        problem += (sell[k, i] <= data['limit'][k][i])

# Storage Capacity Constraints
for k in range(K):
    for i in range(I):
        problem += (storage[k, i] <= 100)

# Final Stock Requirement
for k in range(K):
    problem += (storage[k, I - 1] == data['keep_quantity'])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')