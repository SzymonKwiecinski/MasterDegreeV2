import pulp
import json

# Input data in JSON format
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Parameters
M = len(data['num_machines'])    # Number of machines
K = len(data['profit'])           # Number of products
I = len(data['limit'][0])         # Number of months
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Create the problem
problem = pulp.LpProblem("Manufacturing_and_Maintenance_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("Maintain", ((m, i) for m in range(M) for i in range(I)), cat="Binary")

# Objective Function
problem += (pulp.lpSum(profit[k] * sell[k, i] for k in range(K) for i in range(I)) - 
             pulp.lpSum(store_price * storage[k, i] for k in range(K) for i in range(I))), "Total_Profit"

# Constraints
# Production constraints
for k in range(K):
    for i in range(I):
        problem += manufacture[k, i] <= limit[k][i], f"Production_Limit_Constraint_k{k}_i{i}"

# Inventory balance constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k, i] == (storage[k, i-1] + manufacture[k, i] - sell[k, i]), f"Inventory_Balance_Constraint_k{k}_i{i}"

# Ending inventory requirement
for k in range(K):
    problem += storage[k, I-1] >= keep_quantity, f"Ending_Inventory_Constraint_k{k}"

# Machine availability
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(manufacture[k, i] * time[k][m] for k in range(K)) <= 
                     n_workhours * (24 - down[m])), f"Machine_Availability_Constraint_m{m}_i{i}"

# Non-negativity constraints are already defined by the decision variables' bounds

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')