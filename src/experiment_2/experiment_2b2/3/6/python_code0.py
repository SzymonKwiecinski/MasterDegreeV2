import pulp

# Data
data = {
    'x_0': 0,
    'v_0': 0,
    'x_T': 1,
    'v_T': 0,
    'T': 20
}

x_0 = data['x_0']
v_0 = data['v_0']
x_T = data['x_T']
v_T = data['v_T']
T = data['T']

# Define the problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
a_abs = pulp.LpVariable.dicts("a_abs", range(T), lowBound=0)

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Dynamic constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (a_abs[t] >= a[t])
    problem += (a_abs[t] >= -a[t])

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Objective function
problem += pulp.lpSum(a_abs[t] for t in range(T))

# Solve the problem
problem.solve()

# Extracting the results
result = {
    "x": [pulp.value(x[i]) for i in range(T+1)],
    "v": [pulp.value(v[i]) for i in range(T+1)],
    "a": [pulp.value(a[i]) for i in range(T)],
    "fuel_spend": sum(pulp.value(a_abs[i]) for i in range(T))
}

# Output the results
print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')