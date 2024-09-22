import pulp
import json

# Data provided in JSON format
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Parameters
M = len(data["num_machines"])  # Number of machines
K = len(data["profit"])         # Number of products
I = len(data["limit"][0])      # Number of months
profit = data["profit"]
time = data["time"]
down = data["down"][0]
limit = data["limit"]
store_price = data["store_price"]
keep_quantity = data["keep_quantity"]
n_workhours = data["n_workhours"]

# Create a LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), cat='Binary')

# Objective function
problem += pulp.lpSum(profit[k] * sell[k, i] for k in range(K) for i in range(I)) - pulp.lpSum(store_price * storage[k, i] for k in range(K) for i in range(I))

# Production Time Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(K)) <= n_workhours * (24 - sum(down[j] for j in range(i + 1))), f"Time_Constraint_m{m}_i{i}"

# Marketing Limitations
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= limit[m][i], f"Marketing_Limit_k{k}_i{i}"

# Storage Dynamics
for k in range(K):
    for i in range(1, I):
        problem += storage[k, i] == storage[k, i - 1] + manufacture[k, i] - sell[k, i], f"Storage_Dynamics_k{k}_i{i}"
    problem += storage[k, 0] == 0, f"Initial_Storage_k{k}"

# End-of-Month Stock Requirement
for k in range(K):
    problem += storage[k, I - 1] >= keep_quantity, f"End_Stock_k{k}"

# Maintenance Decision Variables
for m in range(M):
    for i in range(I):
        problem += maintain[m, i] >= 0, f"Maintain_m{m}_i{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')