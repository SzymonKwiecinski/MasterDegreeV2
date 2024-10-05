import pulp
import json

# Data from the provided JSON
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

# Parameters
K = len(data['profit'])  # Number of products
M = len(data['num_machines'])  # Number of machines
I = len(data['limit'][0])  # Number of months

# Create the problem
problem = pulp.LpProblem("ProfitMaximization", pulp.LpMaximize)

# Decision variables
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[(k, i)] - data['store_price'] * storage[(k, i)]
                      for k in range(K) for i in range(I))

# Constraints
# Production and Selling Balance
for k in range(K):
    problem += (manufacture[(k, 0)] + 0 == sell[(k, 0)] + storage[(k, 0)], f"Balance_0_{k}")
    for i in range(1, I):
        problem += (manufacture[(k, i)] + storage[(k, i-1)] == sell[(k, i)] + storage[(k, i)], f"Balance_{i}_{k}")

# Machine Time Constraints
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(data['time'][j][m] * manufacture[(j, i)] for j in range(K)) 
                     <= (data['num_machines'][m] - data['maintain'][m][i]) * 24 * data['n_workhours'], 
                     f"Machine_Time_{m}_{i}")

# Marketing Limitations
for k in range(K):
    for i in range(I):
        problem += (sell[(k, i)] <= data['limit'][k][i], f"Market_Limit_{k}_{i}")

# Storage Limits
for k in range(K):
    for i in range(I):
        problem += (storage[(k, i)] <= 100, f"Storage_Limit_{k}_{i}")

# Stock Requirement at End
for k in range(K):
    problem += (storage[(k, I - 1)] == data['keep_quantity'], f"End_Stock_{k}")

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')