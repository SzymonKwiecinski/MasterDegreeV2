import pulp

# Data from JSON
num_machines = [4, 2, 3, 1, 1]
profit = [10, 6, 8, 4, 11, 9, 3]
time = [
    [0.5, 0.1, 0.2, 0.05, 0.0],
    [0.7, 0.2, 0.0, 0.03, 0.0],
    [0.0, 0.0, 0.8, 0.0, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.0],
    [0.3, 0.0, 0.0, 0.1, 0.05],
    [0.5, 0.0, 0.6, 0.08, 0.05],
    [0.0, 0.0, 0.0, 0.0, 0.05]
]
down = [0, 1, 1, 1, 1]
limit = [
    [500, 600, 300, 200, 0, 500],
    [1000, 500, 600, 300, 100, 500],
    [300, 200, 0, 400, 500, 100],
    [300, 0, 0, 500, 100, 300],
    [800, 400, 500, 200, 1000, 1100],
    [200, 300, 400, 0, 300, 500],
    [100, 150, 100, 100, 0, 60]
]
store_price = 0.5
keep_quantity = 100
n_workhours = 8.0

M = len(num_machines)
K = len(profit)
I = len(limit[0])

# Problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat=pulp.LpInteger)
manufacture = pulp.LpVariable.dicts("Manufacture", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat=pulp.LpInteger)
storage = pulp.LpVariable.dicts("Storage", [(k, i) for k in range(K) for i in range(I)], lowBound=0, upBound=100, cat=pulp.LpInteger)
maintain = pulp.LpVariable.dicts("Maintain", [(m, i) for m in range(M) for i in range(I)], lowBound=0, cat=pulp.LpInteger)

# Objective Function
profit_term = pulp.lpSum(profit[k] * sell[k, i] for k in range(K) for i in range(I))
storage_cost_term = pulp.lpSum(store_price * storage[k, i] for k in range(K) for i in range(I))
problem += profit_term - storage_cost_term

# Constraints
for k in range(K):
    # Storage balance for each product
    problem += storage[k, 0] == manufacture[k, 0] - sell[k, 0]
    for i in range(1, I):
        problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]
    # End stock requirement
    problem += storage[k, I-1] == keep_quantity

    # Sales limits
    for i in range(I):
        problem += sell[k, i] <= limit[k][i]

# Machine availability constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(K)) <= (num_machines[m] - maintain[m, i]) * 24 * 6 * n_workhours

    # Maintenance constraints
    problem += pulp.lpSum(maintain[m, i] for i in range(I)) == down[m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')