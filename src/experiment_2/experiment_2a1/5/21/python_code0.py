import pulp
import json

# Input Data
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

# Parameters
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])

# Create Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("maintain", ((m, k) for m in range(num_machines) for k in range(num_products)), lowBound=0, cat='Binary')

# Objective Function
profit_contribution = pulp.lpSum(data['profit'][k] * sell[(k, i)] for k in range(num_products) for i in range(num_months))
storage_costs = pulp.lpSum(data['store_price'] * storage[(k, i)] for k in range(num_products) for i in range(num_months))

problem += profit_contribution - storage_costs

# Constraints
# Limits
for i in range(num_months):
    for k in range(num_products):
        problem += sell[(k, i)] <= data['limit'][k][i], f"Limit_{k}_{i}"

# Work hours constraints
total_work_hours = data['n_workhours'] * 24 * (6 / 7)
for i in range(num_months):
    for m in range(num_machines):
        available_time = total_work_hours * (1 - data['down'][m])
        problem += pulp.lpSum(data['time'][k][m] * manufacture[(k, i)] for k in range(num_products)) <= available_time, f"Work_hours_{m}_{i}"

# Inventory balance
for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[(k, i)] == storage[(k, i-1)] + manufacture[(k, i)] - sell[(k, i)], f"Inventory_Balance_{k}_{i}"

# Ending stock
for k in range(num_products):
    problem += storage[(k, num_months-1)] >= data['keep_quantity'], f"Ending_Stock_{k}"

# Solve
problem.solve()

# Output Results
sell_result = [[pulp.value(sell[(k, i)]) for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[pulp.value(manufacture[(k, i)]) for k in range(num_products)] for i in range(num_months)]
storage_result = [[pulp.value(storage[(k, i)]) for k in range(num_products)] for i in range(num_months)]
maintain_result = [[pulp.value(maintain[(m, k)]) for m in range(num_machines)] for k in range(num_products)]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result,
    "maintain": maintain_result
}

# Print the objective value
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')