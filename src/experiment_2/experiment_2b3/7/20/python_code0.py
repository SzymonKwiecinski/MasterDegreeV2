import pulp

# Parse the JSON data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'maintain': [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Retrieve data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Constants
num_products = len(profit)
num_machines_type = len(num_machines)
num_months = len(limit[0])

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
manufacture_vars = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat=pulp.LpContinuous)
sell_vars = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat=pulp.LpContinuous)
storage_vars = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat=pulp.LpContinuous)

# Objective function
revenue = pulp.lpSum([profit[k] * sell_vars[(k, i)] - store_price * storage_vars[(k, i)] for k in range(num_products) for i in range(num_months)])
problem += revenue, "Total_Profit"

# Constraints

# Inventory balance
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += (manufacture_vars[(k, i)] == sell_vars[(k, i)] + storage_vars[(k, i)])
        else:
            problem += (manufacture_vars[(k, i)] + storage_vars[(k, i-1)] == sell_vars[(k, i)] + storage_vars[(k, i)])

# Final stock requirement
for k in range(num_products):
    problem += storage_vars[(k, num_months - 1)] >= keep_quantity

# Machine time constraints
for i in range(num_months):
    for m in range(num_machines_type):
        total_available_hours = (num_machines[m] - maintain[i][m]) * n_workhours * 24
        total_time_used = pulp.lpSum([time[k][m] * manufacture_vars[(k, i)] for k in range(num_products)])
        problem += total_time_used <= total_available_hours

# Marketing limitations
for k in range(num_products):
    for i in range(num_months):
        problem += sell_vars[(k, i)] <= limit[k][i]

# Solve the problem
problem.solve()

# Prepare the result
sell_result = [[pulp.value(sell_vars[(k, i)]) for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[pulp.value(manufacture_vars[(k, i)]) for k in range(num_products)] for i in range(num_months)]
storage_result = [[pulp.value(storage_vars[(k, i)]) for k in range(num_products)] for i in range(num_months)]

result = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

# Print results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')