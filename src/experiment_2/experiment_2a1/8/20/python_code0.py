import pulp
import json

# Input data
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

# Extracting data from input
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['maintain'])
profits = data['profit']
times = data['time']
maintenance = data['maintain']
limits = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
total_workhours = n_workhours * 6 * 4  # 6 days a week, approximately 4 weeks a month

# Initializing the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, upBound=None)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, upBound=None)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, upBound=100)

# Objective Function
profit_expr = pulp.lpSum(profits[k] * sell[k, i] for k in range(num_products) for i in range(num_months)) \
              - pulp.lpSum(store_price * storage[k, i] for k in range(num_products) for i in range(num_months))
problem += profit_expr

# Constraints
# Machine time constraints
for i in range(num_months):
    for m in range(num_machines):
        available_time = total_workhours - sum(maintenance[i][m] for i in range(num_months))
        problem += (pulp.lpSum(times[k][m] * manufacture[k, i] for k in range(num_products)) <= available_time)

# Production limits
for k in range(num_products):
    for i in range(num_months):
        problem += (sell[k, i] + storage[k, i] == manufacture[k, i] + (storage[k, i-1] if i > 0 else 0) - keep_quantity)
        problem += (sell[k, i] <= limits[k][i])

# Solve the problem
problem.solve()

# Output results
sell_result = [[pulp.value(sell[k, i]) for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[pulp.value(manufacture[k, i]) for k in range(num_products)] for i in range(num_months)]
storage_result = [[pulp.value(storage[k, i]) for k in range(num_products)] for i in range(num_months)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the results
output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result,
}
print(json.dumps(output))