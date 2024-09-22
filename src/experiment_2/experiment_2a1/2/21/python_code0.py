import json
import pulp

# Input Data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0],
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [1],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500],
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300],
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500],
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Parameters
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines), range(num_months)), lowBound=0, cat='Binary')

# Objective Function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months))
storage_cost_expr = pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_products) for i in range(num_months))
problem += profit_expr - storage_cost_expr, "Total_Profit"

# Constraints
# Production time constraint
for i in range(num_months):
    for m in range(num_machines):
        total_time = pulp.lpSum(data['time[k][m]'] * manufacture[k][i] for k in range(num_products))
        hours_available = data['n_workhours'] * (24 - data['down'][m])  # Working hours considering maintenance
        problem += total_time <= hours_available, f"Machine_Time_Constraint_M{m}_Month{i}"

# Selling limits
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= data['limit'][k][i], f"Sales_Limit_k{k}_i{i}"

# Stock keeping constraints
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[k][i] == data['keep_quantity'], f"Initial_Stock_k{k}"
        else:
            problem += storage[k][i] == storage[k][i - 1] + manufacture[k][i - 1] - sell[k][i - 1] + data['keep_quantity'], f"Stock_Keeping_k{k}_i{i}"

# Solve the problem
problem.solve()

# Output results
sell_results = [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)]
manufacture_results = [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)]
storage_results = [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)]
maintain_results = [[pulp.value(maintain[m][i]) for m in range(num_machines)] for i in range(num_products)]

result = {
    "sell": sell_results,
    "manufacture": manufacture_results,
    "storage": storage_results,
    "maintain": maintain_results
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')