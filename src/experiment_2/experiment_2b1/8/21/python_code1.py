import pulp
import json

data = {'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}

num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
n_months = 6  # Example for 6 months
num_products = len(profit)
num_machines_count = len(num_machines)

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(n_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(n_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(n_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines_count), range(n_months)), lowBound=0, upBound=1, cat='Binary')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(num_products) for i in range(n_months)) - \
           pulp.lpSum(store_price * storage[k][i] for k in range(num_products) for i in range(n_months)), "Total_Profit"

# Constraints
for i in range(n_months):
    for k in range(num_products):
        # Marketing Limitations
        problem += sell[k][i] <= limit[k][i], f"Limit_{k}_{i}"
        # Storage Requirements
        if i > 0:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Storage_Balance_{k}_{i}"

        # Keep Quantity
        if i == n_months - 1:
            problem += storage[k][i] >= keep_quantity, f"Keep_Quantity_{k}"

    # Machine Time Availability
    total_time = pulp.lpSum(manufacture[k][i] * time[k][m] for k in range(num_products) for m in range(num_machines_count) if k < len(time) and m < len(time[0]))
    available_time = (n_workhours * (24 * 6)) * (1 - sum(down[m] for m in range(num_machines_count)))
    problem += total_time <= available_time, f"Machine_Time_Availability_{i}"

# Solve the problem
problem.solve()

# Collect results
sell_result = [[sell[k][i].varValue for k in range(num_products)] for i in range(n_months)]
manufacture_result = [[manufacture[k][i].varValue for k in range(num_products)] for i in range(n_months)]
storage_result = [[storage[k][i].varValue for k in range(num_products)] for i in range(n_months)]
maintain_result = [[maintain[m][k].varValue for m in range(num_machines_count)] for k in range(num_products)]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result,
    "maintain": maintain_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')