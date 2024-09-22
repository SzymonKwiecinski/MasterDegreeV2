import pulp
import json

data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'down': [[0, 1, 1, 1, 1]],
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

K = len(data['profit'])
M = len(data['num_machines'])
I = len(data['limit'][0])

# Create a Linear Programming problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I)) - \
           pulp.lpSum(data['store_price'] * storage[k][i] for k in range(K) for i in range(I))

# Constraints
# Production Time Constraint
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K)) <= \
                   (data['n_workhours'] * (24 - sum(data['down'][0][j] for j in range(i + 1)))) * \
                   (1 - maintain[m][i])

# Sales Limit Constraint
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][k][i]

# Storage Constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]
    problem += storage[k][0] == 0
    problem += storage[k][i] <= 100

# Ending Inventory Constraint
for k in range(K):
    problem += storage[k][I-1] >= data['keep_quantity']

# Solve the problem
problem.solve()

# Output the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')