import pulp

# Parsing the input JSON data
data = {
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    "maintain": [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ],
    "limit": [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0
}

# Constants
num_machines = data["num_machines"]
profits = data["profit"]
time_per_product_machine = data["time"]
machine_maintenance = data["maintain"]
product_limit = data["limit"]
store_price = data["store_price"]
keep_quantity = data["keep_quantity"]
n_workhours_per_day = data["n_workhours"]

# Indices and derived values
num_months = len(machine_maintenance)
num_products = len(profits)
num_types_machines = len(num_machines)
n_workdays_per_month = 24

# Setting up the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(num_products) for i in range(num_months)), 
                             lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), 
                                    lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(num_products) for i in range(num_months)), 
                                lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit_terms = [profits[k] * sell[(k, i)] for k in range(num_products) for i in range(num_months)]
storage_cost_terms = [store_price * storage[(k, i)] for k in range(num_products) for i in range(num_months)]
problem += pulp.lpSum(profit_terms) - pulp.lpSum(storage_cost_terms)

# Constraints

# Initial storage is zero
for k in range(num_products):
    problem += storage[(k, 0)] == manufacture[(k, 0)] - sell[(k, 0)]

# Subsequent storage balance
for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[(k, i)] == storage[(k, i - 1)] + manufacture[(k, i)] - sell[(k, i)]

# Monthly manufacturing, selling, and storage limits
for k in range(num_products):
    for i in range(num_months):
        problem += manufacture[(k, i)] <= product_limit[k][i]
        problem += sell[(k, i)] <= product_limit[k][i]
        problem += storage[(k, i)] <= 100  # storage capacity constraint

# Final storage requirements
for k in range(num_products):
    problem += storage[(k, num_months - 1)] == keep_quantity

# Machine time availability constraints
for i in range(num_months):
    for m in range(num_types_machines):
        machine_hours_available = (num_machines[m] - machine_maintenance[i][m]) * n_workhours_per_day * n_workdays_per_month
        problem += pulp.lpSum(time_per_product_machine[k][m] * manufacture[(k, i)] for k in range(num_products)) <= machine_hours_available

# Solve the problem
problem.solve()

# Output results
sell_result = [[sell[(k, i)].varValue for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[manufacture[(k, i)].varValue for k in range(num_products)] for i in range(num_months)]
storage_result = [[storage[(k, i)].varValue for k in range(num_products)] for i in range(num_months)]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')