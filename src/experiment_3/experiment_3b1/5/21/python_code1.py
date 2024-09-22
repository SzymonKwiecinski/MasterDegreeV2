import pulp
import json

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

M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), lowBound=0, cat='Integer')

# Objective Function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I))
storage_cost_expr = pulp.lpSum(data['store_price'] * storage[k][i] for k in range(K) for i in range(I))
problem += profit_expr - storage_cost_expr

# Constraints

# Production Time Constraints
for i in range(I):
    time_constraint = pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K) for m in range(M))
    problem += time_constraint <= data['n_workhours'] * (M - pulp.lpSum(maintain[m][i] for m in range(M)))

# Market Limitations
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][k][i]

# Storage Constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]
    # Initial condition
    problem += storage[k][0] == 0

# Desired Stock Constraints
for k in range(K):
    problem += storage[k][I-1] >= data['keep_quantity']

# Machine Maintenance Constraints
for i in range(I):
    problem += pulp.lpSum(maintain[m][i] for m in range(M)) <= data['down'][0][i]

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')