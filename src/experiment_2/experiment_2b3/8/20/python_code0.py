from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value
import json

# Define the data
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "maintain": [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Extract data
num_machines = data["num_machines"]
profit = data["profit"]
time = data["time"]
maintain = data["maintain"]
limit = data["limit"]
store_price = data["store_price"]
keep_quantity = data["keep_quantity"]
n_workhours = data["n_workhours"]

# Constants
days_per_month = 24
total_time_available = n_workhours * days_per_month

# Problem dimensions
K = len(profit)  # Number of products
M = len(num_machines)  # Number of machine types
I = len(maintain)  # Number of months

# Define the problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables
sell = [[LpVariable(f"sell_{k}_{i}", lowBound=0, cat='Integer') for k in range(K)] for i in range(I)]
manufacture = [[LpVariable(f"manufacture_{k}_{i}", lowBound=0, cat='Integer') for k in range(K)] for i in range(I)]
storage = [[LpVariable(f"storage_{k}_{i}", lowBound=0, upBound=100, cat='Integer') for k in range(K)] for i in range(I)]

# Objective function
profit_expr = lpSum(profit[k] * sell[i][k] - store_price * storage[i][k] for i in range(I) for k in range(K))
problem += profit_expr

# Constraints
for i in range(I):
    for k in range(K):
        # Production limit by marketing
        problem += sell[i][k] <= limit[k][i]

        # Storage balance
        if i == 0:
            problem += manufacture[i][k] == sell[i][k] + storage[i][k]
        else:
            problem += manufacture[i][k] + storage[i-1][k] == sell[i][k] + storage[i][k]

        # Required storage at the end
        if i == I - 1:
            problem += storage[i][k] >= keep_quantity

    for m in range(M):
        # Machine availability
        available_hours = (num_machines[m] - maintain[i][m]) * total_time_available
        problem += lpSum(time[k][m] * manufacture[i][k] for k in range(K)) <= available_hours

# Solve the problem
problem.solve()

# Results
output = {
    "sell": [[int(value(sell[i][k])) for k in range(K)] for i in range(I)],
    "manufacture": [[int(value(manufacture[i][k])) for k in range(K)] for i in range(I)],
    "storage": [[int(value(storage[i][k])) for k in range(K)] for i in range(I)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')