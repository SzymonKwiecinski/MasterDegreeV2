import pulp

# Data
num_machines = [4, 2, 3, 1, 1]
profit = [10, 6, 8, 4, 11, 9, 3]
time = [
    [0.5, 0.1, 0.2, 0.05, 0.0], 
    [0.7, 0.2, 0.0, 0.03, 0.0], 
    [0.0, 0.0, 0.8, 0.0, 0.01], 
    [0.0, 0.3, 0.0, 0.07, 0.0], 
    [0.3, 0.0, 0.0, 0.1, 0.05], 
    [0.5, 0.0, 0.6, 0.08, 0.05]
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

# Sets
M = list(range(len(num_machines)))
K = list(range(len(profit)))
I = list(range(len(limit[0])))

# Problem
problem = pulp.LpProblem("Manufacturing_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (K, I), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (K, I), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (K, I), lowBound=0, upBound=100)
maintain = pulp.LpVariable.dicts("maintain", (M, I), lowBound=0, cat='Integer')

# Objective
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in K for i in I)

# Constraints
for k in K:
    for i in I:
        problem += sell[k][i] <= limit[k][i]

    # Storage balance constraints
    problem += storage[k][0] == 0
    for i in range(1, len(I)):
        problem += manufacture[k][i] == sell[k][i] + storage[k][i] - storage[k][i-1]
    problem += storage[k][len(I)-1] == keep_quantity

for m in M:
    for i in I:
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in K if k < len(time)) <= (
            (num_machines[m] - maintain[m][i]) * 24 * 6 * n_workhours
        )

    problem += pulp.lpSum(maintain[m][i] for i in I) == down[m]

# Solve
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')