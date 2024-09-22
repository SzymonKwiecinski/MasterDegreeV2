import pulp
import json

# Data from JSON
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], 
              [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], 
              [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], 
              [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Model Setup
problem = pulp.LpProblem("MixedIntegerLinearProgramming", pulp.LpMaximize)

# Parameters
M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
time = data['time']
limit = data['limit']
down = data['down'][0]

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[(k, i)] for k in range(K) for i in range(I)) - \
           pulp.lpSum(store_price * storage[(k, i)] for k in range(K) for i in range(I))

# Production Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[(k, i)] for k in range(K)) <= data['num_machines'][m] * n_workhours

# Sales Limitations
for k in range(K):
    for i in range(I):
        problem += sell[(k, i)] <= limit[k][i]

# Storage Balance
for k in range(K):
    for i in range(1, I):
        problem += storage[(k, i)] == storage[(k, i-1)] + manufacture[(k, i)] - sell[(k, i)]

# Initial Condition for Storage
for k in range(K):
    problem += storage[(k, 0)] == 0

# End of Month Stock Requirement
for k in range(K):
    problem += storage[(k, I-1)] >= keep_quantity

# Maintenance Constraint
for i in range(I):
    problem += pulp.lpSum(maintain[(m, i)] for m in range(M)) <= sum(down)

# Solve the Problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')