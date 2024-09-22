import pulp

# Data extraction from JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extracting the constants
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("RocketOptimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(T + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(1, T + 1), cat='Continuous')
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')

# Objective
problem += M

# Constraints
# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t + 1])

# Target conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Thrust constraints
for t in range(1, T + 1):
    problem += (-M <= a[t])
    problem += (a[t] <= M)

# Solve problem
problem.solve()

# Print objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')