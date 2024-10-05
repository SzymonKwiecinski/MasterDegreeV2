import pulp

# Data input
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'down': [0, 1, 1, 1, 1],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Constants
num_products = len(data['profit'])
num_machines = len(data['num_machines'])
num_months = len(data['limit'][0])
days_per_month = 24
work_hours_per_month = days_per_month * data['n_workhours'] * 2

# Setup the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(num_products), range(num_months+1)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("Maintain", (range(num_machines), range(num_months)), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months))
storage_costs = pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_products) for i in range(num_months))
problem += profit - storage_costs

# Constraints
# Initial storage
for k in range(num_products):
    problem += storage[k][0] == 0

# Storage balance constraint
for k in range(num_products):
    for i in range(1, num_months+1):
        if i < num_months:
            problem += (storage[k][i] == storage[k][i-1] + manufacture[k][i-1] - sell[k][i-1])
        else:
            # Final inventory constraint
            problem += (storage[k][num_months] == data['keep_quantity'])

# Machine time constraints
for m in range(num_machines):
    for i in range(num_months):
        available_hours = (work_hours_per_month * (data['num_machines'][m] - maintain[m][i])) - (data['down'][m] * work_hours_per_month)
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(num_products)) <= available_hours

# Maintenance constraint
for m in range(num_machines):
    problem += pulp.lpSum(maintain[m][i] for i in range(num_months)) == data['down'][m]

# Product limit constraints
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= data['limit'][k][i]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)],
    "maintain": [[pulp.value(maintain[m][i]) for m in range(num_machines)] for i in range(num_months)]
}

# Print the output
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')