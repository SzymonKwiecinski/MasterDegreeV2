import pulp
import json

# Data extraction from JSON format
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "maintain": [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Initialize the problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

# Extract parameters from data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

K = len(profit)  # number of products
I = len(limit)   # number of months
M = len(num_machines)  # number of machines

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective function
problem += pulp.lpSum(profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I)), "Objective_Function"

# Constraints

# Production time constraint
for i in range(I):
    problem += (
        pulp.lpSum(time[m][k] * manufacture[k, i] for k in range(K) for m in range(M)) 
        <= n_workhours * (sum(num_machines) - sum(maintain[i][m] for m in range(M))),
        f"Production_Time_Constraint_{i}"
    )

# Selling constraints
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= limit[i][k], f"Selling_Constraint_{k}_{i}"

# Inventory balance constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i], f"Inventory_Balance_{k}_{i}"

# Storage limits
for k in range(K):
    for i in range(I):
        problem += storage[k, i] <= 100, f"Storage_Limit_{k}_{i}"
        
# Final storage requirement
for k in range(K):
    problem += storage[k, I-1] >= keep_quantity, f"Final_Storage_Requirement_{k}"

# Solve the problem
problem.solve()

# Output results
sell_values = [[sell[k, i].varValue for i in range(I)] for k in range(K)]
manufacture_values = [[manufacture[k, i].varValue for i in range(I)] for k in range(K)]
storage_values = [[storage[k, i].varValue for i in range(I)] for k in range(K)]

print(f'Sell: {sell_values}')
print(f'Manufacture: {manufacture_values}')
print(f'Storage: {storage_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')