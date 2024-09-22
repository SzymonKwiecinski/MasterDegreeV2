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
    [0.5, 0.0, 0.6, 0.08, 0.05]
]
maintain = [
    [1, 0, 0, 0, 1, 0], 
    [0, 0, 0, 1, 1, 0], 
    [0, 2, 0, 0, 0, 1], 
    [0, 0, 1, 0, 0, 0], 
    [0, 0, 0, 0, 0, 1]
]
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

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Sets
K = len(profit)
I = len(limit[0])
M = len(num_machines)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(K), range(I + 1)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(K) for i in range(I))

# Constraints
# Production Time Constraint
for m in range(M):
    problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K) for i in range(I)) <= \
               (num_machines[m] - maintain[m][0]) * n_workhours

# Marketing Limitation
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i]

# Stock Balance Constraint
for k in range(K):
    for i in range(1, I + 1):
        problem += storage[k][i - 1] + manufacture[k][i - 1] - sell[k][i - 1] == storage[k][i]

# Ending Stock Requirement
for k in range(K):
    problem += storage[k][I] >= keep_quantity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')