import pulp

# Parsing input data from JSON
data = {
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    "down": [0, 1, 1, 1, 1],
    "limit": [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0
}

# Constants
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

num_products = len(profit)
num_months = len(limit[0])
num_machine_types = len(num_machines)

work_days_per_month = 24
total_work_hours_per_month = work_days_per_month * n_workhours * 2  # two shifts

# Initialize LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", ((m, i) for m in range(num_machine_types) for i in range(num_months)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum([profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(num_products) for i in range(num_months)])

# Constraints
# Initial stock constraints
for k in range(num_products):
    problem += storage[k, 0] == 0

# End stock requirements
for k in range(num_products):
    problem += storage[k, num_months-1] == keep_quantity

# Stock balance constraint
for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[k, i] == storage[k, i-1] + manufacture[k, i-1] - sell[k, i-1]

# Manufacturing constraints due to machine and time
for i in range(num_months):
    for m in range(num_machine_types):
        problem += pulp.lpSum([time[k][m] * manufacture[k, i] for k in range(num_products)]) <= total_work_hours_per_month * (num_machines[m] - maintain[m, i])

# Maintenance constraints
for m in range(num_machine_types):
    problem += pulp.lpSum([maintain[m, i] for i in range(num_months)]) <= down[m]

# Sales limit constraints
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= limit[k][i]

# Solve the problem
problem.solve()

# Output the results
output = {
    "sell": [[sell[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[manufacture[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    "storage": [[storage[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    "maintain": [[maintain[m, i].varValue for m in range(num_machine_types)] for i in range(num_months)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')