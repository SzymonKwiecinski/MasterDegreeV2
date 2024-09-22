import pulp

# Data input based on provided JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [0, 1, 1, 1, 1],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100],
              [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Extract data variables
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Constants and Dimensions
K = len(profit)  # Number of products
M = len(num_machines)  # Number of machine types
I = len(limit[0])  # Number of months
n_days = 24
work_time_per_month = n_days * 6 * 2 * n_workhours

# Initiate problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", (range(K), range(I)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("Manufacture", (range(K), range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", (range(K), range(I+1)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", (range(M), range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum([profit[k] * sell[k][i] for k in range(K) for i in range(I)]) - \
           pulp.lpSum([store_price * storage[k][i] for k in range(K) for i in range(I)]), "Total Profit"

# Constraints
# Initial storage constraint
for k in range(K):
    problem += storage[k][0] == 0, f"Initial_Storage_Constraint_Prod_{k}"

# Stock at the end of month constraint
for k in range(K):
    problem += storage[k][I] == keep_quantity, f"End_Month_Storage_Prod_{k}"

# Balance constraint
for k in range(K):
    for i in range(I):
        problem += (storage[k][i] + manufacture[k][i] - sell[k][i] == storage[k][i+1],
                    f"Balance_Constraint_Prod_{k}_Month_{i}")

# Marketing limits
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i], f"Marketing_Limit_Prod_{k}_Month_{i}"

# Manufacturing time constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum([time[k][m] * manufacture[k][i] for k in range(K)]) <= (
                    num_machines[m] - maintain[m][i]) * work_time_per_month, \
                   f"Time_Constraint_Machine_{m}_Month_{i}"

# Maintenance constraints
for m in range(M):
    problem += pulp.lpSum([maintain[m][i] for i in range(I)]) == down[m], f"Maintenance_Constraint_Machine_{m}"

# Solve the problem
problem.solve()

# Extract the solution
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[k][i]) for k in range(K)] for i in range(I+1)],
    "maintain": [[pulp.value(maintain[m][i]) for i in range(I)] for m in range(M)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')