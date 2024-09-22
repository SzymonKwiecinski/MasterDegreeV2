import pulp

# Parse the input data
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

# Constants
num_products = len(data['profit'])
num_machines = len(data['num_machines'])
num_months = len(data['maintain'])
days_per_month = 24

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')

# Objective Function: Maximize Profit
profit_expr = pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(num_products) for i in range(num_months))
storage_cost_expr = pulp.lpSum(data['store_price'] * storage[k, i] for k in range(num_products) for i in range(num_months))
problem += profit_expr - storage_cost_expr, "Total_Profit"

# Constraints
# 1. Storage balance constraint
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[k, i] == manufacture[k, i] - sell[k, i]
        else:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]

# 2. End of month storage constraint
for k in range(num_products):
    problem += storage[k, num_months-1] >= data['keep_quantity']

# 3. Limit constraints
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= data['limit'][k][i]

# 4. Machine time constraints
for m in range(num_machines):
    for i in range(num_months):
        available_machines = data['num_machines'][m] - data['maintain'][i][m]
        max_hours = available_machines * data['n_workhours'] * days_per_month
        time_constraint_expr = pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(num_products))
        problem += time_constraint_expr <= max_hours

# Solve the problem
problem.solve()

# Extract the values
solution = {
    "sell": [[int(sell[k, i].varValue) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[int(manufacture[k, i].varValue) for k in range(num_products)] for i in range(num_months)],
    "storage": [[int(storage[k, i].varValue) for k in range(num_products)] for i in range(num_months)]
}

# Print the solution
import json
print(json.dumps(solution, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')