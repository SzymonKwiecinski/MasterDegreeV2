import pulp
import json

# Data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0],
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500],
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300],
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500],
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Indices
K = len(data['profit'])
I = len(data['limit'])
M = len(data['num_machines'])

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), lowBound=0)

# Objective Function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k][i] - data['store_price'] * storage[k][i] for k in range(K) for i in range(I))
problem += profit_expr

# Constraints
# 1. Production capacity constraint on each machine
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(manufacture[k][i] * data['time'][k][m] for k in range(K)) 
                     <= (data['num_machines'][m] - maintain[m][i]) * data['n_workhours'] * 2 * 24)

# 2. Maintenance constraint on each machine
for m in range(M):
    problem += (pulp.lpSum(maintain[m][i] for i in range(I)) == data['down'][0][m])

# 3. Marketing limitation on products
for k in range(K):
    for i in range(I):
        problem += (sell[k][i] <= data['limit'][i][k])

# 4. Inventory balance equation
for k in range(K):
    for i in range(1, I):
        problem += (storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i])

# 5. Initial inventory
for k in range(K):
    problem += (storage[k][0] == 0)

# 6. Final inventory requirement
for k in range(K):
    problem += (storage[k][I-1] == data['keep_quantity'])

# 7. Storage capacity limit
for k in range(K):
    for i in range(I):
        problem += (storage[k][i] <= 100)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')