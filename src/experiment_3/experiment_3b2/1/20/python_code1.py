import pulp
import json

# Data provided in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], 
                 [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Extracting parameters from data
K = len(data['profit'])       # Number of products
M = len(data['num_machines']) # Number of machines
I = len(data['limit'])        # Number of months

# Create the problem variable
problem = pulp.LpProblem("Production_Storage_Optimization", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] 
                       for k in range(K) for i in range(I)), "Total_Profit"

# Constraints
# Market Limitations
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= data['limit'][i][k], f"Market_Limit_k{k}_i{i}"

# Stock Balance
for k in range(K):
    for i in range(1, I):
        problem += storage[k, i-1] + manufacture[k, i] == sell[k, i] + storage[k, i], f"Stock_Balance_k{k}_i{i}"

# Initial storage conditions
for k in range(K):
    problem += storage[k, 0] == 0, f"Initial_Stock_k{k}"

# End of Period Stock Requirement
for k in range(K):
    problem += storage[k, I-1] >= data['keep_quantity'], f"End_Stock_Requirement_k{k}"

# Machine Time Availability
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K)) 
                     <= (data['num_machines'][m] - data['maintain'][i][m]) * 24 * data['n_workhours'], 
                     f"Machine_Time_Availability_m{m}_i{i}")

# Storage Capacity
for k in range(K):
    for i in range(I):
        problem += storage[k, i] <= 100, f"Storage_Capacity_k{k}_i{i}"

# Solve the problem
problem.solve()

# Print the objective value