from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, lpSum, value
import json

# Data input
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
    ],
    "maintain": [
        [1, 0, 0, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 2, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    "limit": [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60],
    ],
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0,
}

# Constants
M = len(data["num_machines"])
K = len(data["profit"])
I = len(data["limit"][0])

# Decision Variables
sell = [[LpVariable(f"sell_{k}_{i}", lowBound=0, cat='Continuous') for i in range(I)] for k in range(K)]
manufacture = [[LpVariable(f"manufacture_{k}_{i}", lowBound=0, cat='Continuous') for i in range(I)] for k in range(K)]
storage = [[LpVariable(f"storage_{k}_{i}", lowBound=0, cat='Continuous') for i in range(I)] for k in range(K)]

# Problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Objective Function
profit_expr = lpSum(
    data["profit"][k] * sell[k][i] - data["store_price"] * storage[k][i]
    for k in range(K)
    for i in range(I)
)
problem += profit_expr

# Constraints
for i in range(I):
    for m in range(M):
        machine_time_constraint = lpSum(
            data["time"][k][m] * manufacture[k][i] for k in range(K) if m < len(data["time"][0])
        ) <= (data["num_machines"][m] - data["maintain"][i][m]) * data["n_workhours"] * 24
        problem += machine_time_constraint

for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data["limit"][k][i]

for k in range(K):
    problem += storage[k][0] == manufacture[k][0] - sell[k][0]
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i - 1] + manufacture[k][i] - sell[k][i]

for k in range(K):
    problem += storage[k][I - 1] >= data["keep_quantity"]

# Solve
problem.solve()

# Outputs
solution = {
    "sell": [[sell[k][i].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[k][i].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[k][i].varValue for k in range(K)] for i in range(I)],
}

print(json.dumps(solution, indent=4))
print(f" (Objective Value): <OBJ>{value(problem.objective)}</OBJ>")