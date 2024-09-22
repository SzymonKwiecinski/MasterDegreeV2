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

# Unpack data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

M = len(num_machines)
K = len(profit)
I = len(limit[0])

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
manufacture = pulp.LpVariable.dicts("Manufacture", (range(I), range(K)), lowBound=0, cat='Integer')
sell = pulp.LpVariable.dicts("Sell", (range(I), range(K)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", (range(I+1), range(K)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", (range(I), range(M)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([
    sell[i][k] * profit[k] - storage[i][k] * store_price
    for i in range(I) for k in range(K)
])

# Constraints
for i in range(I):
    for k in range(K):
        # Selling limits
        problem += sell[i][k] <= limit[k][i], f"Sell_Limit_{i}_{k}"
        # Manufactured products relation with selling and storage
        if i == 0:
            problem += manufacture[i][k] == sell[i][k] + storage[i][k], f"Manufacture_Relation_{i}_{k}"
        else:
            problem += manufacture[i][k] + storage[i-1][k] == sell[i][k] + storage[i][k], f"Manufacture_Relation_{i}_{k}"
            
    for m in range(M):
        # Maintenance constraints
        if i < down[m]:
            problem += maintain[i][m] == num_machines[m], f"Maintenance_{i}_{m}"
        else:
            problem += maintain[i][m] <= num_machines[m], f"Maintenance_{i}_{m}"

    for m in range(M):
        # Working hours constraints per machine
        total_hours = 24 * 6 * n_workhours
        problem += pulp.lpSum([manufacture[i][k] * time[k][m] for k in range(K) if m < len(time[k])]) <= (num_machines[m] - maintain[i][m]) * total_hours, f"Work_Hours_{i}_{m}"

# Final stock requirement
for k in range(K):
    problem += storage[I-1][k] == keep_quantity, f"Final_Stock_{k}"

# Solve problem
problem.solve()

# Extract results
results = {
    "sell": [[int(sell[i][k].varValue) for k in range(K)] for i in range(I)],
    "manufacture": [[int(manufacture[i][k].varValue) for k in range(K)] for i in range(I)],
    "storage": [[int(storage[i][k].varValue) for k in range(K)] for i in range(I+1)],
    "maintain": [[int(maintain[i][m].varValue) for m in range(M)] for i in range(I)]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')