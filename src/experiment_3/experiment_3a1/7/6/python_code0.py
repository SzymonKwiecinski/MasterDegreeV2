import pulp

# Data extraction from the provided JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Problem definition
T = data['TotalTime']
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Dynamics_Optimization", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: minimize total fuel consumed
problem += pulp.lpSum([pulp.lpSum([a[t], -a[t]]) for t in range(T)])

# Initial conditions
x[0] = x0
v[0] = v0

# Dynamics constraints
for t in range(T - 1):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]

# Target conditions
problem += x[T] == xT
problem += v[T] == vT

# Solve the problem
problem.solve()

# Output results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]

# Total fuel spent
fuel_spent = sum(abs(acc) for acc in accelerations)

# Print results
print(f'Positions: {positions}')
print(f'Velocities: {velocities}')
print(f'Accelerations: {accelerations}')
print(f'Fuel spent: {fuel_spent}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')