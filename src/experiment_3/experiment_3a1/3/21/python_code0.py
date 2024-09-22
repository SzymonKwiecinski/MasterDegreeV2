import pulp
import json

# Data from JSON
data = {'num_machines': [4, 2, 3, 1, 1], 
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
        'n_workhours': 8.0}

# Constants
num_m = len(data['num_machines'])  # Number of machines
num_k = len(data['profit'])         # Number of products
num_i = len(data['limit'][0])       # Number of months

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_k), range(num_i)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_k), range(num_i)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(num_k), range(num_i)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(num_m), range(num_i)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_k) for i in range(num_i)) \
           - pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_k) for i in range(num_i))

# Constraints
# Production Time Constraint
for m in range(num_m):
    for i in range(num_i):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(num_k)) \
                   <= data['n_workhours'] * 6 * 24 - pulp.lpSum(maintain[m][i+j] for j in range(data['down'][0][m]))

# Storage Constraint
for k in range(num_k):
    for i in range(1, num_i):  # Start from month 1
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

# Set initial storage
for k in range(num_k):
    problem += storage[k][0] == 0  # Initial stock

# Marketing Limitations
for k in range(num_k):
    for i in range(num_i):
        problem += sell[k][i] <= data['limit'][k][i]

# Desired End-of-Month Stock
for k in range(num_k):
    problem += storage[k][num_i-1] >= data['keep_quantity']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')