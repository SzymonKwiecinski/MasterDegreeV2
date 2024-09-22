import pulp
import json

# Input data
data = {'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3],
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
        'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}

num_products = len(data['profit'])
num_months = len(data['limit'][0])
num_machines = len(data['num_machines'])

# Create the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([data['profit'][k] * sell[k, i] for k in range(num_products) for i in range(num_months)]) - pulp.lpSum([data['store_price'] * storage[k, i] for k in range(num_products) for i in range(num_months)])

# Constraints
# Storage balance constraints
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[k, i] == data['keep_quantity'] + manufacture[k, i] - sell[k, i], f"Storage_Balance_Product_{k}_Month_{i}"
        else:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i], f"Storage_Balance_Product_{k}_Month_{i}"

# Production time constraints
for i in range(num_months):
    for m in range(num_machines):
        available_hours = data['n_workhours'] * (24 - sum(data['maintain'][i][m] for i in range(num_months)))
        problem += pulp.lpSum([data['time[k][m]'] * manufacture[k, i] for k in range(num_products)]) <= available_hours, f"Time_Constraint_Machine_{m}_Month_{i}"

# Selling limit constraints
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= data['limit'][k][i], f"Selling_Limit_Product_{k}_Month_{i}"

# keep_quantity constraint for each product at the end of last month
for k in range(num_products):
    problem += storage[k, num_months - 1] >= data['keep_quantity'], f"Keep_Quantity_Product_{k}"

# Solve the problem
problem.solve()

# Output results
sell_result = [[sell[k, i].varValue for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[manufacture[k, i].varValue for k in range(num_products)] for i in range(num_months)]
storage_result = [[storage[k, i].varValue for k in range(num_products)] for i in range(num_months)]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')