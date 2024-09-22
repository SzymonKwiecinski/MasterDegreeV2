import pulp

# Data received
data = {
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05],
        [0.2, 0.4, 0.6, 0.0, 0.1]  # Added missing data for the seventh product
    ],
    "down": [[0, 1, 1, 1, 1]],
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

# Parameters
num_m = len(data['num_machines'])
num_k = len(data['profit'])
num_i = len(data['limit'][0])

# Decision Variables
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

manufacture = pulp.LpVariable.dicts("Manufacture", (range(num_k), range(num_i)), lowBound=0, cat='Integer')
sell = pulp.LpVariable.dicts("Sell", (range(num_k), range(num_i)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", (range(num_k), range(num_i+1)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", (range(num_m), range(num_i)), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum(
    [
        sell[k][i] * data['profit'][k] - storage[k][i] * data['store_price']
        for k in range(num_k) for i in range(num_i)
    ]
)
problem += profit

# Constraints
for k in range(num_k):
    for i in range(num_i):
        problem += sell[k][i] <= data['limit'][k][i], f"Limit_Sell_{k}_{i}"
        problem += manufacture[k][i] + storage[k][i] == sell[k][i] + storage[k][i + 1], f"Balance_{k}_{i}"

    problem += storage[k][0] == 0, f"Init_Storage_{k}"
    problem += storage[k][num_i] == data['keep_quantity'], f"End_Storage_{k}"

for m in range(num_m):
    for i in range(num_i):
        available_hours = (data['num_machines'][m] - maintain[m][i]) * 24 * data['n_workhours']
        used_hours = pulp.lpSum([manufacture[k][i] * data['time'][k][m] for k in range(num_k) if m < len(data['time'][k])])
        problem += used_hours <= available_hours, f"Machine_Hours_{m}_{i}"

# Maintenance Constraint
for m in range(num_m):
    total_down = pulp.lpSum([maintain[m][i] for i in range(num_i)])
    problem += total_down == data['down'][0][m], f"Maintenance_{m}"

# Solve the problem
problem.solve()

# Output the results
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(num_k)] for i in range(num_i)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(num_k)] for i in range(num_i)],
    "storage": [[pulp.value(storage[k][i]) for k in range(num_k)] for i in range(num_i+1)],
    "maintain": [[pulp.value(maintain[m][i]) for m in range(num_m)] for i in range(num_i)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')