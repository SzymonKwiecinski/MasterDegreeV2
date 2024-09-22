import pulp
import json

# Input data
data = {
    'num_machines': [4, 2, 3, 1, 1],
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
    'n_workhours': 8.0
}

# Problem setup
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", ((m, k) for m in range(num_machines) for k in range(num_products)), lowBound=0, cat='Binary')

# Objective function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(num_products) for i in range(num_months)) - pulp.lpSum(data['store_price'] * storage[k, i] for k in range(num_products) for i in range(num_months))
problem += profit_expr

# Constraints
# Maintenance constraints
for m in range(num_machines):
    for i in range(num_months):
        problem += pulp.lpSum(maintain[m, k] for k in range(num_products)) <= data['down'][0], f"Max_Maintenance_{m}_{i}"

# Production and sell limits
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= data['limit'][k][i], f"Sell_Limit_{k}_{i}"
        problem += manufacture[k, i] <= data['limit'][k][i], f"Manufacture_Limit_{k}_{i}"

# Storage to maintain keep quantity
for k in range(num_products):
    for i in range(num_months - 1):
        problem += storage[k, i] + manufacture[k, i] - sell[k, i] >= storage[k, i+1] - data['keep_quantity'], f"Storage_{k}_{i}"

# Total working hours constraint
for i in range(num_months):
    total_time = pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(num_products) for m in range(num_machines))
    problem += total_time <= data['n_workhours'] * 24 * 6 * (1 - data['down'][0]), f"Time_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
results = {
    "sell": [[sell[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[manufacture[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    "storage": [[storage[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    "maintain": [[maintain[m, k].varValue for k in range(num_products)] for m in range(num_machines)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print results
print(json.dumps(results, indent=2))