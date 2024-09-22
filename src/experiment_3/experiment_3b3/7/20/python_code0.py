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
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'maintain': [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ],
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

# Constants
K = len(data['profit'])
I = len(data['limit'][0])
M = len(data['num_machines'])

# Linear Problem
problem = pulp.LpProblem("Engineering_Factory", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i]
    for k in range(K) for i in range(I)
)

# Constraints
# (1) Sales must not exceed marketing limits
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= data['limit'][k][i]

# (2) Storage condition for each month based on manufacture and sales
for k in range(K):
    for i in range(I):
        if i == 0:
            problem += storage[k, i] == manufacture[k, i] - sell[k, i]
        else:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]

# (3) Storage must not exceed the maximum capacity
for k in range(K):
    for i in range(I):
        problem += storage[k, i] <= 100

# (4) Manufacture is limited by machine availability and production time
for k in range(K):
    for i in range(I):
        available_machines = sum(data['num_machines'][m] for m in range(M))
        available_hours = data['n_workhours'] * (6 * 24 * available_machines - sum(data['maintain'][m][i] for m in range(M)))
        max_manufacture = pulp.lpSum(
            available_hours / data['time'][k][m]
            for m in range(M) if data['time'][k][m] > 0
        )
        problem += manufacture[k, i] <= max_manufacture

# (5) End-month storage must meet the desired quantity
for k in range(K):
    problem += storage[k, I-1] >= data['keep_quantity']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')