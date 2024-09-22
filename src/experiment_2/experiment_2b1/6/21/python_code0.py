import pulp
import json

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

num_machines = data['num_machines']
profits = data['profit']
times = data['time']
down = data['down'][0]
limits = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
months = len(limits[0])  # number of months
products = len(profits)  # number of products
machines = len(num_machines)  # number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(products), range(months)), 0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(products), range(months)), 0)
storage = pulp.LpVariable.dicts("storage", (range(products), range(months)), 0)
maintain = pulp.LpVariable.dicts("maintain", (range(machines), range(months)), 0, cat='Integer')

# Objective Function
problem += pulp.lpSum([profits[k] * sell[k][i] for k in range(products) for i in range(months)]) - \
          pulp.lpSum([store_price * storage[k][i] for k in range(products) for i in range(months)])

# Constraints
for i in range(months):
    for k in range(products):
        # Selling limit per month
        problem += sell[k][i] <= limits[k][i]
    
    # Machine maintenance
    total_downtime = sum([down[m] for m in range(machines)]) 
    available_time = n_workhours * (24 * 6 - total_downtime)  # Total available work hours in the month
    problem += pulp.lpSum([times[k][m] * manufacture[k][i] for k in range(products) for m in range(machines)]) <= available_time

    # Storage and keep quantity
    for k in range(products):
        if i > 0:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]
        problem += storage[k][i] >= keep_quantity

# Solve the problem
problem.solve()

# Collect results
result_sell = [[pulp.value(sell[k][i]) for k in range(products)] for i in range(months)]
result_manufacture = [[pulp.value(manufacture[k][i]) for k in range(products)] for i in range(months)]
result_storage = [[pulp.value(storage[k][i]) for k in range(products)] for i in range(months)]
result_maintain = [[pulp.value(maintain[m][i]) for m in range(machines)] for i in range(products)]

# Output results
output = {
    "sell": result_sell,
    "manufacture": result_manufacture,
    "storage": result_storage,
    "maintain": result_maintain
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')