import pulp

# Data input
data = {
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    "maintain": [[1, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 2, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]],
    "limit": [[500, 600, 300, 200, 0], [1000, 500, 600, 300, 100], [300, 200, 0, 400, 500], [300, 0, 0, 500, 100], [800, 400, 500, 200, 1000], [200, 300, 400, 0, 300], [100, 150, 100, 100, 0]],
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0
}

num_machines = data["num_machines"]
profit = data["profit"]
time = data["time"]
maintain = data["maintain"]
limit = data["limit"]
store_price = data["store_price"]
keep_quantity = data["keep_quantity"]
n_workhours = data["n_workhours"]

K = len(profit)
M = len(num_machines)
I = len(maintain)

# Problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

# Variables
manufacture = pulp.LpVariable.dicts("manufacture", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
sell = pulp.LpVariable.dicts("sell", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[(k, i)] - store_price * storage[(k, i)] for k in range(K) for i in range(I))

# Constraints
work_hours = 6 * n_workhours * 24

for i in range(I):
    for k in range(K):
        if i == 0:
            problem += manufacture[(k, i)] == sell[(k, i)] + storage[(k, i)]
        else:
            problem += manufacture[(k, i)] + storage[(k, i-1)] == sell[(k, i)] + storage[(k, i)]
        problem += sell[(k, i)] <= limit[k][i]
        problem += storage[(k, i)] <= 100

for i in range(I):
    for m in range(M):
        problem += pulp.lpSum(time[k][m] * manufacture[(k, i)] for k in range(K)) <= (num_machines[m] - maintain[i][m]) * work_hours

for k in range(K):
    problem += storage[(k, I-1)] >= keep_quantity

# Solve the problem
problem.solve()

output = {
    "sell": [[sell[(k, i)].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[(k, i)].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[(k, i)].varValue for k in range(K)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')