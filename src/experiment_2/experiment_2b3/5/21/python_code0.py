import pulp

# Load data
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

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

num_machines = data['num_machines']
profits = data['profit']
times = data['time']
down_times = data['down']
limits = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Indices
K = len(profits)
M = len(num_machines)
I = len(limits[0])

# Variables
manufacture = pulp.LpVariable.dicts("Manufacture", (range(K), range(I)), lowBound=0, cat='Integer')
sell = pulp.LpVariable.dicts("Sell", (range(K), range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", (range(K), range(I+1)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", (range(M), range(I)), lowBound=0, upBound=1, cat='Integer')

# Objective function
profit_terms = [
    profits[k] * sell[k][i] - store_price * storage[k][i]
    for k in range(K) for i in range(I)
]
problem += pulp.lpSum(profit_terms), "Total_Profit"

# Constraints
# Inventory balance constraints
for k in range(K):
    problem += storage[k][0] == 0  # No initial stock
    for i in range(I):
        problem += storage[k][i+1] == manufacture[k][i] - sell[k][i] + storage[k][i]

# Final required storage constraint
for k in range(K):
    problem += storage[k][I] == keep_quantity

# Production constraints based on machine time and availability
work_hours_per_month = 6 * 2 * n_workhours * 24

for i in range(I):
    for m in range(M):
        machine_time_constraints = [
            times[k][m] * manufacture[k][i] for k in range(K)
        ]
        problem += pulp.lpSum(machine_time_constraints) <= (num_machines[m] - maintain[m][i]) * work_hours_per_month
        problem += pulp.lpSum(maintain[m][i] for m in range(M)) >= down_times[m]

# Sales constraints
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limits[k][i]

# Solve the problem
problem.solve()

# Output results
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[k][i]) for k in range(K)] for i in range(I + 1)],
    "maintain": [[pulp.value(maintain[m][i]) for m in range(M)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')