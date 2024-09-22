import pulp
import json

# Data in JSON format
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

# Extracting parameters
M = len(data['num_machines'])  # Total number of machines
K = len(data['profit'])         # Total number of products
I = len(data['limit'][0])      # Total number of months

num_m = data['num_machines']   # Number of machines available
profit_k = data['profit']       # Profit per unit for each product
time_k_m = data['time']         # Production time for each product on each machine
maintain_i_m = data['maintain'] # Maintenance status
limit_k_i = data['limit']       # Selling limits
store_price = data['store_price']# Cost of storing each unit
keep_quantity = data['keep_quantity'] # Required stock at the end of month
n_workhours = data['n_workhours']      # Working hours per day

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)  # Amount sold
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)  # Amount manufactured
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)  # Amount stored

# Objective Function
problem += pulp.lpSum(profit_k[k] * sell[k][i] for k in range(K) for i in range(I)) - \
           pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I)), "Total_Profit"

# Production Time Constraint
for i in range(I):
    problem += pulp.lpSum(time_k_m[k][m] * manufacture[k][i] for k in range(K) for m in range(M)) <= \
               (n_workhours * 6 * 24 - pulp.lpSum(maintain_i_m[i][m] for m in range(M)), f"Time_Constraint_{i}")

# Selling Limits
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit_k_i[k][i], f"Selling_Limits_{k}_{i}"

# Storage Balance Constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Storage_Balance_{k}_{i}"

# Initial storage condition
for k in range(K):
    problem += storage[k][0] == 0, f"Initial_Storage_{k}"

# End-of-Month Stock Requirement
for k in range(K):
    problem += storage[k][I-1] >= keep_quantity, f"End_Stock_Requirement_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')