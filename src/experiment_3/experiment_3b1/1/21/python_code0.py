import pulp
import json

# Data provided in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0],
             [0.7, 0.2, 0.0, 0.03, 0.0],
             [0.0, 0.0, 0.8, 0.0, 0.01],
             [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05],
             [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [[500, 600, 300, 200, 0, 500],
              [1000, 500, 600, 300, 100, 500],
              [300, 200, 0, 400, 500, 100],
              [300, 0, 0, 500, 100, 300],
              [800, 400, 500, 200, 1000, 1100],
              [200, 300, 400, 0, 300, 500],
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Defining parameters
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
profits = data['profit']
time = data['time']
down_times = data['down'][0]
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Create the optimization problem
problem = pulp.LpProblem("Engineering_Factory_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(num_machines) for i in range(num_months)), lowBound=0)

# Objective Function
problem += pulp.lpSum(profits[k] * sell[k, i] for k in range(num_products) for i in range(num_months)) - \
           pulp.lpSum(store_price * storage[k, i] for k in range(num_products) for i in range(num_months))

# Constraints

# Production Time Constraint
for i in range(num_months):
    for m in range(num_machines):
        available_time = n_workhours * (24 - down_times[m])
        problem += pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(num_products)) <= available_time

# Sales Limit Constraint
for i in range(num_months):
    for k in range(num_products):
        problem += sell[k, i] <= data['limit'][k][i]

# Storage Balance
for i in range(1, num_months):
    for k in range(num_products):
        problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]

# Desired Ending Stock
for k in range(num_products):
    problem += storage[k, num_months - 1] >= keep_quantity

# Non-negativity Constraints already defined in variable creation

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')