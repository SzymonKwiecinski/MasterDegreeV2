import pulp
import json

# Given data in JSON format
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Parameters
K = len(data['profit'])    # Number of products
I = len(data['limit'])     # Number of months
M = len(data['num_machines'])  # Number of machines
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Create the problem variable
problem = pulp.LpProblem("Production_Planning", pulp.LpMaximize)

# Decision Variables:
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

# Objective Function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I))
storage_cost_expr = pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I))
problem += profit_expr - storage_cost_expr

# Constraints
# Inventory balance
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i-1] + manufacture[k][i] == sell[k][i] + storage[k][i]

# Initial condition
for k in range(K):
    problem += storage[k][0] == 0

# Production capacity constraint
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time'][i][k] * manufacture[k][i] for k in range(K)) <= n_workhours * 2 * 24 * 6 * (data['num_machines'][m] - pulp.lpSum(maintain[m][j] for j in range(i + 1)))

# Marketing limitation
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][i][k]

# Storage limitation
for k in range(K):
    for i in range(I):
        problem += storage[k][i] <= 100

# End inventory requirement
for k in range(K):
    problem += storage[k][I-1] == keep_quantity

# Maintenance constraint
for m in range(M):
    problem += pulp.lpSum(maintain[m][i] for i in range(I)) == data['down'][0][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')