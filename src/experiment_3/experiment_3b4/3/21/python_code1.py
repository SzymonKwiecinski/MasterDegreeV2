import pulp

# Data
num_machines = [4, 2, 3, 1, 1]
profit = [10, 6, 8, 4, 11, 9, 3]
time = [[0.5, 0.1, 0.2, 0.05, 0.0], 
        [0.7, 0.2, 0.0, 0.03, 0.0], 
        [0.0, 0.0, 0.8, 0.0, 0.01], 
        [0.0, 0.3, 0.0, 0.07, 0.0], 
        [0.3, 0.0, 0.0, 0.1, 0.05], 
        [0.5, 0.0, 0.6, 0.08, 0.05]]
down = [0, 1, 1, 1, 1]
limit = [[500, 600, 300, 200, 0, 500],
         [1000, 500, 600, 300, 100, 500],
         [300, 200, 0, 400, 500, 100],
         [300, 0, 0, 500, 100, 300],
         [800, 400, 500, 200, 1000, 1100],
         [200, 300, 400, 0, 300, 500],
         [100, 150, 100, 100, 0, 60]]
store_price = 0.5
keep_quantity = 100
n_workhours = 8.0

# Parameters
M = len(num_machines)
K = len(profit)
I = len(limit[0]) - 1  # Adjusted to get the correct limit for I

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I+1)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I))

# Constraints
# Initial conditions
for k in range(K):
    problem += storage[k, 0] == 0

# Manufacturing balance
for k in range(K):
    for i in range(I):
        problem += (storage[k, i] + manufacture[k, i] == sell[k, i] + storage[k, i+1])

# End stock requirement
for k in range(K):
    problem += storage[k, I] == keep_quantity

# Machine availability
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(manufacture[k, i] * time[k][m] for k in range(K) if k < len(time))  # Add condition to prevent IndexError
                    <= (num_machines[m] - maintain[m, i]) * 24 * 6 * n_workhours)

# Maintenance requirement
for m in range(M):
    problem += pulp.lpSum(maintain[m, i] for i in range(I)) == down[m] * num_machines[m]

# Marketing limits
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= limit[k][i]

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')