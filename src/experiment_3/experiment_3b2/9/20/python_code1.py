import pulp
import json

# Load data from JSON format.
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "maintain": [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Parameters
num_months = len(data['time'])
num_products = len(data['profit'])
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Create the Linear Program
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')  # Production
s = pulp.LpVariable.dicts("s", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')  # Storage
y = pulp.LpVariable.dicts("y", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')  # Sales

# Objective function
problem += pulp.lpSum((profit[k] * y[k, i] - store_price * s[k, i]) for k in range(num_products) for i in range(num_months))

# Production Time Constraints
for m in range(len(num_machines)):
    for i in range(num_months):
        problem += (pulp.lpSum(time[i][k] * x[k, i] for k in range(num_products)) <= (num_machines[m] - maintain[m][i]) * n_workhours * 24)

# Market Limitations
for k in range(num_products):
    for i in range(num_months):
        problem += (y[k, i] <= limit[k][i])

# Storage Balance
for k in range(num_products):
    for i in range(1, num_months):
        problem += (s[k, i] == s[k, i - 1] + x[k, i] - y[k, i])

# Initialize storage at the beginning
for k in range(num_products):
    problem += (s[k, 0] == 0)

# Storage Capacity
for k in range(num_products):
    for i in range(num_months):
        problem += (s[k, i] <= 100)

# End of Planning Requirement
for k in range(num_products):
    problem += (s[k, num_months - 1] == keep_quantity)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')