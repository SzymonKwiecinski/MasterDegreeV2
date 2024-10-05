import pulp
import json

# Data provided in JSON format
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

# Parameters
M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])  # Assuming months correspond to the number of limits given
n_workhours = data['n_workhours']
store_price = data['store_price']
keep_quantity = data['keep_quantity']

# Create the model
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - store_price * storage[k, i] 
                       for k in range(K) for i in range(I))

# Constraints

# Production constraints for each machine
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K)) <= \
                   (data['num_machines'][m] - maintain[m, i]) * 2 * n_workhours * 24

# Maintenance constraints
for m in range(M):
    problem += pulp.lpSum(maintain[m, i] for i in range(I)) == data['down'][0][m]

# Marketing limits
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= data['limit'][k][i]

# Inventory balance
for k in range(K):
    for i in range(1, I):
        problem += storage[k, i] == storage[k, i - 1] + manufacture[k, i] - sell[k, i]

# Initial storage condition
for k in range(K):
    problem += storage[k, 0] == 0

# Ending stock requirement
for k in range(K):
    problem += storage[k, I - 1] >= keep_quantity

# Storage capacity
for k in range(K):
    for i in range(I):
        problem += storage[k, i] <= 100

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')