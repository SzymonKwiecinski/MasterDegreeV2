import pulp
import json

# Given data in JSON format
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

# Extract parameters from the data
M = len(data['num_machines'])  # Number of machines
K = len(data['profit'])         # Number of products
I = len(data['limit'][0])       # Number of months

# Create the problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Define decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in range(K) for i in range(I)), "Total_Profit"

# Production Constraints
for i in range(I):
    for m in range(M):
        problem += (pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K)) <= 
                    (data['num_machines'][m] - maintain[m, i]) * 24 * data['n_workhours']), f"Production_Constraint_m{m}_month{i}"

# Maintenance Constraints
for m in range(M):
    problem += (pulp.lpSum(maintain[m, i] for i in range(I)) == data['down'][0][m]), f"Maintenance_Constraint_m{m}"

# Storage and Balance Constraints
for k in range(K):
    problem += (storage[k, 0] == 0), f"Initial_Storage_k{k}"
    for i in range(1, I):
        problem += (storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]), f"Balance_Constraint_k{k}_month{i}"
    problem += (storage[k, I-1] == data['keep_quantity']), f"Final_Storage_Constraint_k{k}"

# Market Limitation Constraints
for k in range(K):
    for i in range(I):
        problem += (sell[k, i] <= data['limit'][k][i]), f"Market_Limit_k{k}_month{i}"

# Storage Capacity Constraints
for k in range(K):
    for i in range(I):
        problem += (storage[k, i] <= 100), f"Storage_Capacity_k{k}_month{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')