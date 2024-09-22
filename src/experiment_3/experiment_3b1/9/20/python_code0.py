import pulp
import json

# Load data from the provided JSON format
data = json.loads("""
{
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    "maintain": [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]],
    "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]],
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0
}
""")

# Extract data from the loaded JSON
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

M = len(num_machines)
K = len(profit)
I = len(limit)

# Create a Linear Programming problem
problem = pulp.LpProblem("Factory_Production_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    problem += pulp.lpSum(sum(time[k][m] * manufacture[k, i] for m in range(M)) for k in range(K)) <= n_workhours * (6 * 24 - sum(maintain[i][m] for m in range(M))), f"ProdTimeConstraint_{i}"

for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= limit[i][k], f"MarketingLimit_{k}_{i}"

for k in range(K):
    for i in range(I):
        problem += storage[k, i] <= 100, f"StorageLimit_{k}_{i}"

for k in range(K):
    for i in range(I):
        problem += storage[k, i] + manufacture[k, i] - sell[k, i] == keep_quantity, f"EndingInventoryRequirement_{k}_{i}"

# Solve the problem
problem.solve()

# Print the results
sell_results = [[sell[k, i].varValue for k in range(K)] for i in range(I)]
manufacture_results = [[manufacture[k, i].varValue for k in range(K)] for i in range(I)]
storage_results = [[storage[k, i].varValue for k in range(K)] for i in range(I)]

print(f"Sell: {sell_results}")
print(f"Manufacture: {manufacture_results}")
print(f"Storage: {storage_results}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')