import pulp
import json

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

num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
n_workhours = data['n_workhours']
months_per_year = 6  # The number of months considered is limited, here assumed to be 6 as per the limit data

# Define the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0)

# Objective Function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(num_products) for i in range(num_months)) - \
              pulp.lpSum(data['store_price'] * storage[k, i] for k in range(num_products) for i in range(num_months))
problem += profit_expr

# Constraints
# Manufacturing time constraints
for i in range(num_months):
    work_time = pulp.lpSum(data['time[k][m]'] * manufacture[k, i] for k in range(num_products) for m in range(num_machines)) 
    problem += work_time <= n_workhours * (num_machines - sum(data['maintain'][i]))

# Selling and storage limits
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] + storage[k, i] == manufacture[k, i] + (storage[k, i-1] if i > 0 else 0)
        problem += sell[k, i] <= data['limit'][k][i]

# Storage constraints to ensure we keep enough stock
for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[k, i] >= data['keep_quantity']

# Solve the problem
problem.solve()

# Prepare the results
sell_result = [[pulp.value(sell[k, i]) for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[pulp.value(manufacture[k, i]) for k in range(num_products)] for i in range(num_months)]
storage_result = [[pulp.value(storage[k, i]) for k in range(num_products)] for i in range(num_months)]

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Prepare output in required format
output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

print(json.dumps(output, indent=4))