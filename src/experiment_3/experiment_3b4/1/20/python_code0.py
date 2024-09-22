import pulp

# Data
num_machines = [4, 2, 3, 1, 1]
profit = [10, 6, 8, 4, 11, 9, 3]
time = [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], 
        [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]]
maintain = [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]]
limit = [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
         [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], 
         [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]]
store_price = 0.5
keep_quantity = 100
n_workhours = 8.0

# Sets
K = range(len(profit))
I = range(len(limit[0]))
M = range(len(num_machines))

# Create LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (K, I), lowBound=0, upBound=100, cat='Continuous')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in K for i in I)

# Constraints
for k in K:
    for i in I:
        if i == 0:
            problem += manufacture[k][i] == sell[k][i] + storage[k][i]
        else:
            problem += storage[k][i-1] + manufacture[k][i] == sell[k][i] + storage[k][i]

for m in M:
    for i in I:
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in K) <= (num_machines[m] - maintain[m][i]) * 24 * n_workhours

for k in K:
    for i in I:
        problem += sell[k][i] <= limit[k][i]

for k in K:
    problem += storage[k][I[-1]] >= keep_quantity

# Solve problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')