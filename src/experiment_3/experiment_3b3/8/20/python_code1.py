import pulp

# Data from JSON
num_machines = [4, 2, 3, 1, 1]
profit = [10, 6, 8, 4, 11, 9, 3]
time = [
    [0.5, 0.1, 0.2, 0.05, 0.0],
    [0.7, 0.2, 0.0, 0.03, 0.0],
    [0.0, 0.0, 0.8, 0.0, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.0],
    [0.3, 0.0, 0.0, 0.1, 0.05],
    [0.5, 0.0, 0.6, 0.08, 0.05]
]
maintain = [
    [1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 2, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1]
]
limit = [
    [500, 600, 300, 200, 0, 500],
    [1000, 500, 600, 300, 100, 500],
    [300, 200, 0, 400, 500, 100],
    [300, 0, 0, 500, 100, 300],
    [800, 400, 500, 200, 1000, 1100],
    [200, 300, 400, 0, 300, 500],
    [100, 150, 100, 100, 0, 60]
]
store_price = 0.5
keep_quantity = 100
n_workhours = 8.0

# Constants
num_products = len(profit)
num_months = len(limit[0])
num_machine_types = len(num_machines)

# Problem definition
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')

# Objective Function
profit_expr = pulp.lpSum(profit[k] * sell[(k, i)] for k in range(num_products) for i in range(num_months))
storage_cost_expr = pulp.lpSum(store_price * storage[(k, i)] for k in range(num_products) for i in range(num_months))
problem += profit_expr - storage_cost_expr

# Constraints

# Production Time Constraints
for i in range(num_months):
    problem += pulp.lpSum(time[k][m] * manufacture[(k, i)] for k in range(num_products) for m in range(num_machine_types)) <= (n_workhours * (6 * 24 - sum(maintain[i][m] for m in range(num_machine_types))))

# Marketing Limits Constraints
for k in range(num_products):
    for i in range(num_months):
        problem += sell[(k, i)] <= limit[k][i]

# Storage Calculation Constraints
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[(k, i)] == manufacture[(k, i)] - sell[(k, i)]
        else:
            problem += storage[(k, i)] == storage[(k, i-1)] + manufacture[(k, i)] - sell[(k, i)]

# Ending Inventory Requirement
for k in range(num_products):
    problem += storage[(k, num_months - 1)] >= keep_quantity

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')