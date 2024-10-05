import pulp

# Data
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
    'down': [1, 1, 1, 1, 1],  # Changed to correct format
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

# Problem Parameters
num_machines = data['num_machines']
profit = data['profit']
time_required = data['time']
down = data['down']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
days_per_month = 24

K = len(profit)  # number of products
M = len(num_machines)  # number of machines
I = len(limit[0])  # number of months

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I))

# Constraints

# Production constraints
for i in range(I):
    for m in range(M):
        problem += pulp.lpSum(time_required[k][m] * manufacture[k, i] for k in range(K)) <= \
                   (num_machines[m] - (down[m] if i < down[m] else 0)) * n_workhours * 6 * days_per_month

# Maintenance constraints
for m in range(M):
    problem += pulp.lpSum(maintain[m, i] for i in range(I)) == down[m]

# Limit constraints
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= limit[k][i]

# Storage constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            problem += manufacture[k, i] == sell[k, i] + storage[k, i]
        else:
            problem += manufacture[k, i] + storage[k, i - 1] == sell[k, i] + storage[k, i]
    problem += storage[k, I - 1] == keep_quantity

# Solve the problem
problem.solve()

# Results
output = {
    "sell": [[sell[k, i].varValue for i in range(I)] for k in range(K)],
    "manufacture": [[manufacture[k, i].varValue for i in range(I)] for k in range(K)],
    "storage": [[storage[k, i].varValue for i in range(I)] for k in range(K)],
    "maintain": [[maintain[m, i].varValue for i in range(I)] for m in range(M)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')