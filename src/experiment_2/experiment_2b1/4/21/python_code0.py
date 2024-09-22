import pulp
import json

data = {'num_machines': [4, 2, 3, 1, 1], 
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
        'n_workhours': 8.0}

num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
down_months = data['down'][0]

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines), range(num_months)), lowBound=0, upBound=1, cat='Binary')

# Objective Function
profit_per_product = [data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months)]
cost_per_storage = data['store_price'] * sum(storage[k][i] for k in range(num_products) for i in range(num_months))
problem += pulp.lpSum(profit_per_product) - cost_per_storage

# Constraints
# Production and sales limits
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= data['limit'][k][i]
        
# Storage balance
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[k][i] == manufacture[k][i] - sell[k][i] + data['keep_quantity']
        else:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i] + data['keep_quantity']

# Machine availability
for i in range(num_months):
    total_time_used = pulp.lpSum(manufacture[k][i] * data['time'][k][m] for k in range(num_products) for m in range(num_machines))
    total_available_time = (data['n_workhours'] * (24 * 6)) * (1 - sum(down_months[:i+1]))  # Hours available minus downtime
    problem += total_time_used <= total_available_time

# Solve the problem
problem.solve()

# Output results
sell_result = [[sell[k][i].varValue for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[manufacture[k][i].varValue for k in range(num_products)] for i in range(num_months)]
storage_result = [[storage[k][i].varValue for k in range(num_products)] for i in range(num_months)]
maintain_result = [[maintain[m][i].varValue for m in range(num_machines)] for i in range(num_months)]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result,
    "maintain": maintain_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')