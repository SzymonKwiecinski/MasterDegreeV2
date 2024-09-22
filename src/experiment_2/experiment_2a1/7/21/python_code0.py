import pulp
import json

# Input data in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [1, 1, 1, 1, 1],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Parameters
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
n_workhours = data['n_workhours'] * 6 * 4  # Total working hours in a month

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), 0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), 0)
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), 0)
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines), range(num_months)), 0)

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months)) \
            - pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_products) for i in range(num_months))

# Constraints

# Production capacity constraint
for m in range(num_machines):
    for i in range(num_months):
        if i >= data['down'][m]:  # Machine is available for production
            problem += pulp.lpSum(data['time[k][m]'] * manufacture[k][i] for k in range(num_products)) <= n_workhours

# Marketing limits constraint
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= data['limit'][k][i]

# Storage limits constraint
for k in range(num_products):
    for i in range(num_months):
        if i > 0:  # From second month onwards
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

# Keeping quantity at the end of month
for k in range(num_products):
    problem += storage[k][num_months-1] >= data['keep_quantity']

# Solve the problem
problem.solve()

# Prepare output data
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)],
    "maintain": [[pulp.value(maintain[m][i]) for m in range(num_machines)] for i in range(num_months)]
}

# Print out the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')