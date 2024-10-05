import pulp

# Reading data from input
data = {
    "x_0": 0,
    "v_0": 0,
    "x_T": 1,
    "v_T": 0,
    "T": 20
}

# Extract data
x_0 = data['x_0']
v_0 = data['v_0']
x_T = data['x_T']
v_T = data['v_T']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("RocketOptimization", pulp.LpMinimize)

# Create variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]

# Set the objective function to minimize the total fuel spent
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)])

# Add initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Add final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Add the dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])

# Solve the problem
problem.solve()

# Prepare the output in the specified format
output = {
    "x": [pulp.value(x[t]) for t in range(T+1)],
    "v": [pulp.value(v[t]) for t in range(T+1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": sum(pulp.value(pulp.lpAbs(a[t])) for t in range(T))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')