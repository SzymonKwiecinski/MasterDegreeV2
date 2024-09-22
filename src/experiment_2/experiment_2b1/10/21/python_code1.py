import json
import pulp

# Input data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0],
             [0.7, 0.2, 0.0, 0.03, 0.0],
             [0.0, 0.0, 0.8, 0.0, 0.01],
             [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05],
             [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [1, 1, 1, 1, 1],
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
I = len(data['limit'][0])  # Number of months
K = len(data['profit'])  # Number of products
M = len(data['num_machines'])  # Number of machines

sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(K) for i in range(I)) - \
           pulp.lpSum(data['store_price'] * storage[k, i] for k in range(K) for i in range(I)), "Total_Profit"

# Constraints
for i in range(I):
    for k in range(K):
        # Selling limit
        problem += sell[k, i] <= data['limit'][k][i], f"Limit_{k}_{i}"
        
        # Storage requirement
        if i > 0:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i] + data['keep_quantity'], f"Storage_Requirement_{k}_{i}"
        else:
            problem += storage[k, i] == manufacture[k, i] - sell[k, i] + data['keep_quantity'], f"Storage_Requirement_{k}_{i}"

for i in range(I):
    for m in range(M):
        if data['down'][m] > 0 and i < data['down'][m]:
            # Machines under maintenance
            problem += maintain[m, i] == 1, f"Maintenance_{m}_{i}"
        else:
            problem += maintain[m, i] >= 0, f"Available_Machines_{m}_{i}"
        
    # Time constraint for manufacturing
    total_time = pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K) for m in range(M))
    problem += total_time <= data['n_workhours'] * (M - pulp.lpSum(maintain[m, i] for m in range(M))), f"Time_Constraint_{i}"

# Solve the problem
problem.solve()

# Extracting results
result = {
    "sell": [[pulp.value(sell[k, i]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[k, i]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[k, i]) for k in range(K)] for i in range(I)],
    "maintain": [[pulp.value(maintain[m, i]) for m in range(M)] for i in range(I)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')