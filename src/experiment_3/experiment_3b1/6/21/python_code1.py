import pulp
import json

# Data input
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Extracting parameters from data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Constants
M = len(num_machines)  # number of machines
K = len(profit)        # number of products
I = len(limit[0])      # number of months

# Model
problem = pulp.LpProblem("Manufacturing_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(K) for i in range(I)) - pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I))

# Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K) if m < len(time[k])) <= n_workhours * (1 - down[m]), f"Production_Time_Constraint_m{m}_i{i}"

for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i], f"Marketing_Limit_k{k}_i{i}"

for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Inventory_Balance_k{k}_i{i}"

for k in range(K):
    problem += storage[k][0] == 0, f"Initial_Storage_k{k}"

for k in range(K):
    problem += storage[k][I-1] >= keep_quantity, f"Desired_Ending_Inventory_k{k}"

# Non-negativity and binary constraints
for k in range(K):
    for i in range(I):
        problem += sell[k][i] >= 0
        problem += manufacture[k][i] >= 0
        problem += storage[k][i] >= 0

for m in range(M):
    for i in range(I):
        problem += maintain[m][i] in [0, 1]

# Solve the problem
problem.solve()

# Output the results
for k in range(K):
    for i in range(I):
        print(f'sell_{k}_{i}: {sell[k][i].varValue}, manufacture_{k}_{i}: {manufacture[k][i].varValue}, storage_{k}_{i}: {storage[k][i].varValue}')

for m in range(M):
    for i in range(I):
        print(f'maintain_{m}_{i}: {maintain[m][i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')