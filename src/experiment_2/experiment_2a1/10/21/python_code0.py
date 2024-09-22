import json
import pulp

# Data input from the given format
data = {'num_machines': [4, 2, 3, 1, 1], 
        'profit': [10, 6, 8, 4, 11, 9, 3], 
        'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
                 [0.7, 0.2, 0.0, 0.03, 0.0], 
                 [0.0, 0.0, 0.8, 0.0, 0.01], 
                 [0.0, 0.3, 0.0, 0.07, 0.0], 
                 [0.3, 0.0, 0.0, 0.1, 0.05], 
                 [0.5, 0.0, 0.6, 0.08, 0.05]], 
        'down': [1], 
        'limit': [[500, 600, 300, 200, 0, 500], 
                  [1000, 500, 600, 300, 100, 500], 
                  [300, 200, 0, 400, 500, 100], 
                  [300, 0, 0, 500, 100, 300], 
                  [800, 400, 500, 200, 1000, 1100], 
                  [200, 300, 400, 0, 300, 500], 
                  [100, 150, 100, 100, 0, 60]], 
        'store_price': 0.5, 
        'keep_quantity': 100, 
        'n_workhours': 8.0}

# Extracting data from the input
num_machines = data["num_machines"]
profits = data["profit"]
time = data["time"]
down = data["down"][0]
limits = data["limit"]
store_price = data["store_price"]
keep_quantity = data["keep_quantity"]
n_workhours = data["n_workhours"]

# Constants
num_products = len(profits)
num_months = len(limits[0])
num_machines_available = sum(num_machines) - sum(down)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0)

# Objective Function
problem += pulp.lpSum([profits[k] * sell[k][i] for k in range(num_products) for i in range(num_months)]) - \
           pulp.lpSum([store_price * storage[k][i] for k in range(num_products) for i in range(num_months)])

# Constraints
for i in range(num_months):
    for k in range(num_products):
        problem += sell[k][i] <= limits[k][i]
        problem += (manufacture[k][i] + storage[k][i-1] if i > 0 else 0) - sell[k][i] == storage[k][i] - keep_quantity

for i in range(num_months):
    total_time_available = num_machines_available * n_workhours * 24
    problem += (pulp.lpSum([time[k][m] * manufacture[k][i] for k in range(num_products) for m in range(len(num_machines))]) <= total_time_available)

# Solving the problem
problem.solve()

# Output the solution
sell_result = [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)]
storage_result = [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)]
maintain_result = [[down for _ in range(num_products)] for _ in range(num_months)]  # All machines down is a placeholder

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result,
    "maintain": maintain_result
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')