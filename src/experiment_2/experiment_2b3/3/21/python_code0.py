import pulp

# Data
data = {
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    "down": [0, 1, 1, 1, 1],
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

# Constants
M = len(data["num_machines"])
K = len(data["profit"])
I = len(data["limit"][0])
work_hours_per_month = 24 * 6 * data["n_workhours"]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I+1)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, upBound=1, cat='Binary')

# Objective
problem += pulp.lpSum(data["profit"][k] * sell[k, i] - data["store_price"] * storage[k, i] for k in range(K) for i in range(I))

# Constraints

# Storage continuity
for i in range(I):
    for k in range(K):
        if i == 0:
            problem += storage[k, i] == manufacture[k, i] - sell[k, i]
        else:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]

# Final storage requirement
for k in range(K):
    problem += storage[k, I] >= data["keep_quantity"]

# Machine maintenance
for m in range(M):
    problem += pulp.lpSum(maintain[m, i] for i in range(I)) == data["down"][m]

# Production time on machines
for i in range(I):
    for m in range(M):
        problem += (
            pulp.lpSum(data["time"][k][m] * manufacture[k, i] for k in range(K)) <= 
            data["num_machines"][m] * work_hours_per_month * (1 - maintain[m, i])
        )

# Marketing limits
for i in range(I):
    for k in range(K):
        problem += sell[k, i] <= data["limit"][k][i]

# Solve
problem.solve()

# Output
output = {
    "sell": [[sell[k, i].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[k, i].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[k, i].varValue for k in range(K)] for i in range(I)],
    "maintain": [[maintain[m, i].varValue for m in range(M)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')