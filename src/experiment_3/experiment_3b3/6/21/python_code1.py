import pulp

# Problem data
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
down = [[0, 1, 1, 1, 1]]
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
hours_per_month = n_workhours * 24

num_products = len(profit)
num_months = len(limit[0])
num_machine_types = len(num_machines)

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(num_machine_types), range(num_months)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(num_products) for i in range(num_months)])

# Constraints

# Production Time Constraint
for m in range(num_machine_types):
    for i in range(num_months):
        available_time = hours_per_month * num_machines[m] - down[0][m] * hours_per_month
        problem += pulp.lpSum([time[k][m] * manufacture[k][i] for k in range(len(time))]) <= available_time

# Marketing Limitation Constraint
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= limit[k][i]

# Storage Balance Constraint
for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]
    # Initial month storage constraint
    problem += storage[k][0] == manufacture[k][0] - sell[k][0]

# Final Stock Requirement
for k in range(num_products):
    problem += storage[k][num_months - 1] >= keep_quantity

# Maintenance Limits
for i in range(num_months):
    problem += pulp.lpSum([maintain[m][i] for m in range(num_machine_types)]) <= sum(num_machines)

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')