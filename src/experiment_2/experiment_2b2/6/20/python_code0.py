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
    'maintain': [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ],
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
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

K = len(profit)
M = len(num_machines)
I = len(maintain)

# Problem
problem = pulp.LpProblem("Manufacturing_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum([
    profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I)
])

# Constraints
for i in range(I):
    for m in range(M):
        machine_availability = num_machines[m] - maintain[i][m]
        problem += pulp.lpSum([time[k][m] * manufacture[k, i] for k in range(K)]) <= machine_availability * 24 * n_workhours, f"Machine_Capacity_M{m+1}_Month{i+1}"

for i in range(I):
    for k in range(K):
        if i > 0:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i], f"Storage_Balance_K{k+1}_Month{i+1}"
        else:
            problem += storage[k, i] == manufacture[k, i] - sell[k, i], f"Initial_Storage_Balance_K{k+1}"

for i in range(I):
    for k in range(K):
        problem += sell[k, i] <= limit[k][i], f"Limit_K{k+1}_Month{i+1}"

for k in range(K):
    problem += storage[k, I-1] == keep_quantity, f"End_Storage_K{k+1}"

# Solve
problem.solve()

# Output
output = {
    "sell": [[int(sell[k, i].varValue) for k in range(K)] for i in range(I)],
    "manufacture": [[int(manufacture[k, i].varValue) for k in range(K)] for i in range(I)],
    "storage": [[int(storage[k, i].varValue) for k in range(K)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')