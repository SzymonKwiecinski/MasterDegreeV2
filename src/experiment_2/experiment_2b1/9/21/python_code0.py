import pulp
import json

# Input data in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]],
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

# Model parameters
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = 6  # Number of months we consider

# Create a Linear Program
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(num_machines) for i in range(num_months)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(num_products) for i in range(num_months)) - \
           pulp.lpSum(data['store_price'] * storage[k, i] for k in range(num_products) for i in range(num_months)), "Total_Profit"

# Constraints
# Sell limits based on market limits
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= data['limit'][k][i], f"Limit_{k}_{i}"

# Storage constraint
for k in range(num_products):
    for i in range(num_months):
        problem += storage[k, i] <= sell[k, i] + manufacture[k, i] - data['keep_quantity'], f"Storage_{k}_{i}"

# Manufacturing time constraint
total_workhours = (data['n_workhours'] * 6 * 24)  # Total hours available in a month
for i in range(num_months):
    for m in range(num_machines):
        if data['down'][m]:
            continue
            
        problem += pulp.lpSum(manufacture[k, i] * data['time'][k][m] for k in range(num_products)) <= total_workhours, f"WorkHours_{m}_{i}"

# Solve the problem
problem.solve()

# Output results
result = {
    "sell": [[pulp.value(sell[k, i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k, i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k, i]) for k in range(num_products)] for i in range(num_months)],
    "maintain": [[pulp.value(maintain[m, i]) for m in range(num_machines)] for i in range(num_months)]
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')