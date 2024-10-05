import pulp

# Data from JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Define variables
T = data['TotalTime']
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Position variables
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocity variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=-pulp.lpInfinity)  # Acceleration variables

# Create the LP problem
problem = pulp.LpProblem("RocketFuelMinimization", pulp.LpMinimize)

# Objective function: Minimize total fuel spent
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)])

# Initial conditions
problem += (x[0] == data['InitialPosition'])
problem += (v[0] == data['InitialVelocity'])

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Boundary conditions
problem += (x[T] == data['FinalPosition'])
problem += (v[T] == data['FinalVelocity'])

# Solve the problem
problem.solve()

# Output the results
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]

print(f'Positions: {positions}')
print(f'Velocities: {velocities}')
print(f'Accelerations: {accelerations}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')