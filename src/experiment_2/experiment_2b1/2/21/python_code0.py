import pulp
import json

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
    'down': [[0, 1, 1, 1, 1]],
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

num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines), range(num_months)), lowBound=0, cat='Integer')

# Objective function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months))
storage_cost_expr = pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_products) for i in range(num_months))

problem += profit_expr - storage_cost_expr, "Total_Profit"

# Constraints
total_hours = data['n_workhours'] * 24 * 6   # total working hours in a month

# Machine constraints
for m in range(num_machines):
    for i in range(num_months):
        if data['down'][0][m] > 0:
            effective_hours = total_hours * (1 - (1 / data['down'][0][m]))  # under maintenance, reduce hours
        else:
            effective_hours = total_hours
        problem += pulp.lpSum(data['time[k][m]' for k in range(num_products)] * manufacture[k][i] for k in range(num_products)) <= effective_hours, f"Machine_{m+1}_Month_{i+1}"

# Product limits
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= data['limit'][k][i], f"Limit_Product_{k+1}_Month_{i+1}"

# Storage constraints
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[k][i] == manufacture[k][i] - sell[k][i] + data['keep_quantity'], f"Initial_Storage_Product_{k+1}_Month_{i+1}"
        else:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Storage_Product_{k+1}_Month_{i+1}"

# Solve the problem
problem.solve()

# Extracting the results
result = {
    "sell": [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)],
    "maintain": [[pulp.value(maintain[m][k]) for m in range(num_machines)] for k in range(num_products)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')