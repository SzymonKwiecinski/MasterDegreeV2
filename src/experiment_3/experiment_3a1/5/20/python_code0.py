import pulp
import json

# Data provided in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]], 
    'maintain': [[1, 0, 0, 0, 1, 0], 
                 [0, 0, 0, 1, 1, 0], 
                 [0, 2, 0, 0, 0, 1], 
                 [0, 0, 1, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 1]], 
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

# Parameters
M = len(data['num_machines'])  # Number of machines
K = len(data['profit'])         # Number of products
I = len(data['limit'])          # Number of months

# Create the problem
problem = pulp.LpProblem("Engineering_Factory_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] - data['store_price'] * storage[k][i] 
                      for k in range(K) for i in range(I))

# Production Time Constraint
for i in range(I):
    problem += (pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K) for m in range(M)) <= 
                 (data['n_workhours'] * 6 * 24) - 
                 pulp.lpSum(data['maintain'][i][m] * data['n_workhours'] * 6 * 24 for m in range(M)))

# Marketing Limitation Constraint
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][i][k]

# Storage Constraint
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

# Initial storage
for k in range(K):
    problem += storage[k][0] == 0

# End Stock Constraint
for k in range(K):
    for i in range(I):
        problem += storage[k][i] >= data['keep_quantity']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')