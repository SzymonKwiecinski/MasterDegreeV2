import pulp
import json

# Input Data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], 
                 [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Constants
num_months = len(data['maintain'])
num_products = len(data['profit'])
num_machines = len(data['num_machines'])
total_hours_per_month = data['n_workhours'] * 6 * 24

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months)) - \
             pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_products) for i in range(num_months))

# Constraints

# Machine time constraints
for i in range(num_months):
    for m in range(num_machines):
        available_time = total_hours_per_month - sum(data['maintain'][i][m] for i in range(num_months))
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(num_products)) <= available_time

# Selling limits
for i in range(num_months):
    for k in range(num_products):
        problem += sell[k][i] <= data['limit'][k][i]

# Storage constraints
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[k][i] == data['keep_quantity'] - sell[k][i] + manufacture[k][i]
        else:
            problem += storage[k][i] == storage[k][i - 1] - sell[k][i] + manufacture[k][i]

# Solve the problem
problem.solve()

# Collect results
results = {
    "sell": [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)]
}

# Output results
print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')