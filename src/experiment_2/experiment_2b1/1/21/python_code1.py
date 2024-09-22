import pulp
import json

# Input data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [1, 1, 1, 1, 1],
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

# Parameters extraction
num_products = len(data['profit'])
num_months = len(data['limit'][0])
num_machines = len(data['num_machines'])
n_workhours = data['n_workhours']
total_workhours = n_workhours * 24 * 6  # 24 days, 6 days a week

# Create the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
maintain = pulp.LpVariable.dicts("Maintain", (m for m in range(num_machines)), lowBound=0, cat='Integer')

# Objective function
profit_per_product = pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(num_products) for i in range(num_months))
storage_cost = pulp.lpSum(data['store_price'] * storage[k, i] for k in range(num_products) for i in range(num_months))

problem += profit_per_product - storage_cost

# Constraints
# Production time constraint
for i in range(num_months):
    for m in range(num_machines):
        total_time = pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(num_products))
        problem += total_time <= total_workhours * (1 - maintain[m])  # as machine goes down

# Selling and storage constraints
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= data['limit'][k][i]
        problem += manufacture[k, i] + (storage[k, i-1] if i > 0 else 0) - sell[k, i] == storage[k, i] + data['keep_quantity']

# Solve the problem
problem.solve()

# Output results
sell_result = [[pulp.value(sell[k, i]) for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[pulp.value(manufacture[k, i]) for k in range(num_products)] for i in range(num_months)]
storage_result = [[pulp.value(storage[k, i]) for k in range(num_products)] for i in range(num_months)]
maintain_result = [[pulp.value(maintain[m]) for m in range(num_machines)]]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result,
    "maintain": maintain_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')