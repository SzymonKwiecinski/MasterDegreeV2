import pulp

# Data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Constants
M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
total_hours_per_month = n_workhours * 6 * 24

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("Sell", (range(K), range(I)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("Manufacture", (range(K), range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", (range(K), range(I)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", (range(M), range(I)), lowBound=0, cat='Integer')

# Objective Function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I))
storage_cost_expr = pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I))
problem += profit_expr - storage_cost_expr

# Constraints
# Machine capacity and maintenance
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K)) <= \
                   (data['num_machines'][m] - maintain[m][i]) * total_hours_per_month
        problem += maintain[m][i] <= data['down'][0][m]

# Marketing limits and storage balance
for k in range(K):
    for i in range(I):
        if i == 0:
            problem += manufacture[k][i] == sell[k][i] + storage[k][i]
        else:
            problem += manufacture[k][i] + storage[k][i-1] == sell[k][i] + storage[k][i]
        problem += sell[k][i] <= data['limit'][k][i]
        if i == I-1:
            problem += storage[k][i] >= keep_quantity

# Solve
problem.solve()

# Output
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[k][i]) for k in range(K)] for i in range(I)],
    "maintain": [[pulp.value(maintain[m][i]) for m in range(M)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')