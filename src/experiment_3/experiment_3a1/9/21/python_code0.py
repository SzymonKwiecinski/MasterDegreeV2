import pulp
import json

# Load data from JSON
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Parameters
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

M = len(num_machines)  # number of machines
K = len(profit)        # number of products
I = len(limit[0])      # number of months

# Initialize the problem
problem = pulp.LpProblem("Manufacturing_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for i in range(I) for k in range(K)) - \
           pulp.lpSum(store_price * storage[k][i] for i in range(I) for k in range(K))

# Constraints

# Production Time Constraint
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(manufacture[k][i] * time[k][m] for k in range(K)) <= \
                   n_workhours * (24 * 6) * (1 - down[m] / I)

# Marketing Limit Constraint
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[m][i]

# Storage Constraint
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

# Initial storage condition
for k in range(K):
    problem += storage[k][0] == 0

# Ending Stock Requirement
for k in range(K):
    problem += storage[k][I-1] >= keep_quantity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')