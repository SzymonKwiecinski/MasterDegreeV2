import json
import pulp

# Data input
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

# Problem parameters
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
num_workhours = data['n_workhours'] * 6 * 24  # Total work hours in the month
store_price = data['store_price']
maintain = data['maintain']
profit = data['profit']
time = data['time']
limit = data['limit']
keep_quantity = data['keep_quantity']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(num_products) for i in range(num_months)) \
            - pulp.lpSum(store_price * storage[k][i] for k in range(num_products) for i in range(num_months)), "Total_Profit"

# Constraints
# Machine availability and production limits
for i in range(num_months):
    total_available_time = num_workhours - sum(maintain[i][m] * 24 for m in range(num_machines))
    for m in range(num_machines):
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(num_products) if m < len(time[k])) <= total_available_time, f"Machine_Time_Constraint_{i}_{m}")

    for k in range(num_products):
        if i > 0:
            problem += sell[k][i] + storage[k][i-1] <= manufacture[k][i] + storage[k][i], f"Storage_Constraint_{k}_{i}"

for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= limit[k][i], f"Limit_Constraint_{k}_{i}"

# Keep quantity constraints
for k in range(num_products):
    problem += storage[k][num_months - 1] >= keep_quantity, f"Keep_Quantity_{k}"

# Solve the problem
problem.solve()

# Collect results
sell_result = [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)]
storage_result = [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Final output
output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

output