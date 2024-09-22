import pulp
import json

# Load the data from the provided JSON format
data = json.loads("{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}")

# Define parameters
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Define indices
M = len(num_machines)  # Total number of machines
K = len(profit)        # Total number of products
I = len(limit[0])      # Total number of months

# Create the problem
problem = pulp.LpProblem("Engineering_Factory_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(K), range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("Maintain", (range(M), range(I)), cat='Binary')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(K) for i in range(I)) - pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I))

# Constraints
# Production Capacity
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K)) <= n_workhours * 12 * (1 - down[m]), f"Prod_Capacity_Machine_{m}_Month_{i}"

# Sales Limits
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i], f"Sales_Limit_Product_{k}_Month_{i}"

# Storage Balance
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Storage_Balance_Product_{k}_Month_{i}"

# End-of-Month Inventory
for k in range(K):
    problem += storage[k][I-1] >= keep_quantity, f"End_Inventory_Product_{k}"

# Maintenance Scheduling
for m in range(M):
    for i in range(I):
        if i + down[m] < I:  # Ensure we don't exceed the range
            problem += pulp.lpSum(maintain[m][j] for j in range(i, i + down[m] + 1)) <= 1, f"Maintenance_Schedule_Machine_{m}_Month_{i}"

# Solve the Problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')