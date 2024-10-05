import pulp

# Input data
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

num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

K = len(profit)  # Number of products
M = len(num_machines)  # Number of machine types
I = len(limit[0])  # Number of months

max_hours_per_month = n_workhours * 2 * 6 * 24  # 6 days a week, 2 shifts, 24 days

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", (range(K), range(I)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("Manufacture", (range(K), range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", (range(K), range(I)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", (range(M), range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(K) for i in range(I)) - \
           pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I)), "Total Profit"

# Constraints

# Production time constraints on machines
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K)) <= \
                   (num_machines[m] - maintain[m][i]) * max_hours_per_month

# Maintenance constraints
for m in range(M):
    problem += pulp.lpSum(maintain[m][i] for i in range(I)) == down[m]

# Marketing limits and inventory balance constraints
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i]
        if i == 0:
            problem += manufacture[k][i] == sell[k][i] + storage[k][i]
        else:
            problem += manufacture[k][i] + storage[k][i-1] == sell[k][i] + storage[k][i]

# Final inventory constraints
for k in range(K):
    problem += storage[k][I-1] == keep_quantity

# Solve problem
problem.solve()

# Prepare output
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[k][i]) for k in range(K)] for i in range(I)],
    "maintain": [[pulp.value(maintain[m][i]) for m in range(M)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')