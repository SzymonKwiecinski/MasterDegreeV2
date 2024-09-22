import pulp
import json

# Data provided
data_json = '''{
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]], 
    "maintain": [[1, 0, 0, 0, 1, 0], 
                 [0, 0, 0, 1, 1, 0], 
                 [0, 2, 0, 0, 0, 1], 
                 [0, 0, 1, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 1]], 
    "limit": [[500, 600, 300, 200, 0, 500], 
              [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], 
              [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], 
              [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]], 
    "store_price": 0.5, 
    "keep_quantity": 100, 
    "n_workhours": 8.0
}'''

data = json.loads(data_json)

# Defining the problem
problem = pulp.LpProblem("Production_Management", pulp.LpMaximize)

I = len(data['limit'][0])  # Number of products
K = len(data['profit'])  # Number of machine types
M = len(data['num_machines'])  # Number of machines

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
z = pulp.LpVariable.dicts("z", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
profit_expr = pulp.lpSum(data['profit'][k] * y[k, i] - data['store_price'] * z[k, i] for k in range(K) for i in range(I))
problem += profit_expr, "Total_Profit"

# Constraints

# Production Constraints
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(data['time'][k][m] * x[k, i] for k in range(K)) <= 
                     (data['num_machines'][m] - data['maintain'][m][i]) * data['n_workhours'] * 60), f"Production_Constraint_{m}_{i}"

# Demand Constraints
for k in range(K):
    for i in range(I):
        problem += (y[k, i] <= data['limit'][k][i]), f"Demand_Constraint_{k}_{i}"

# Inventory Balance Constraints
for k in range(K):
    for i in range(1, I):
        problem += (z[k, i] == z[k, i-1] + x[k, i] - y[k, i]), f"Inventory_Balance_{k}_{i}"

# Storage Constraints
for k in range(K):
    for i in range(I):
        problem += (z[k, i] <= 100), f"Storage_Constraint_{k}_{i}"

# Final Month Stock Requirement
for k in range(K):
    problem += (z[k, I-1] == data['keep_quantity']), f"Final_Stock_Requirement_{k}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')