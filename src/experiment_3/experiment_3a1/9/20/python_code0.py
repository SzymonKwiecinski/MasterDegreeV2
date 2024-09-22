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

# Extracting data from the JSON-like data structure
num_m = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])  # assuming limit has data for each month

profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(K) for i in range(I))

# Constraints
# Production Time Constraint
for i in range(I):
    constraint_expr = pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K) for m in range(num_m))
    available_time = n_workhours * (sum(data['num_machines']) - sum(maintain[i][m] for m in range(num_m)))
    problem += constraint_expr <= available_time

# Marketing Limitation
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i]

# Storage Constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i - 1] + manufacture[k][i] - sell[k][i]
    # Initial storage for month 1
    problem += storage[k][0] == 0

# Ending Inventory Requirement
for k in range(K):
    problem += storage[k][I - 1] >= keep_quantity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')