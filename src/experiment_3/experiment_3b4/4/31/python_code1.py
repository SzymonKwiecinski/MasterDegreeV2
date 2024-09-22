import pulp

# Data from JSON
demand = [15000, 30000, 25000, 40000, 27000]
num = [12, 10, 5]
minlevel = [850, 1250, 1500]
maxlevel = [2000, 1750, 4000]
runcost = [1000, 2600, 3000]
extracost = [2.0, 1.3, 3.0]
startcost = [2000, 1000, 500]

# Problem
problem = pulp.LpProblem("GeneratorScheduling", pulp.LpMinimize)

# Sets
T = len(demand)
K = len(num)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat=pulp.LpInteger)
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat=pulp.LpBinary)
p = pulp.LpVariable.dicts("p", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat=pulp.LpContinuous)

# Objective Function
problem += pulp.lpSum(
    x[k, t] * runcost[k] + p[k, t] * extracost[k] + y[k, t] * startcost[k]
    for k in range(K) for t in range(T)
)

# Constraints
# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(x[k, t] * minlevel[k] + p[k, t] for k in range(K)) == demand[t]

# Power output constraints
for k in range(K):
    for t in range(T):
        problem += p[k, t] <= x[k, t] * (maxlevel[k] - minlevel[k])

# Upper bound on the number of generators
for k in range(K):
    for t in range(T):
        problem += x[k, t] <= num[k]

# Generator start-up indication
for k in range(K):
    for t in range(1, T):
        problem += y[k, t] >= (x[k, t] - x[k, t - 1]) / num[k]
    # Initial condition for first time period
    problem += y[k, 0] >= x[k, 0] / float(num[k])  # Changed to float

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')