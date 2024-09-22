import pulp

# Given data 
data = {'InitialPosition': 0, 
        'InitialVelocity': 0, 
        'FinalPosition': 1, 
        'FinalVelocity': 0, 
        'TotalTime': 20}

# Extract data
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create the problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # Acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocity

# Objective function: Minimize fuel used (sum of absolute accelerations)
problem += pulp.lpSum([pulp.lpSum([a[t] for t in range(T)])]), "TotalFuel"

# Initial conditions
problem += x[0] == x0, "InitialPosition"
problem += v[0] == v0, "InitialVelocity"

# Dynamic equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionConstraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityConstraint_{t}"

# Final conditions
problem += x[T] == xT, "FinalPosition"
problem += v[T] == vT, "FinalVelocity"

# Solve the problem
problem.solve()

# Collect results
positions = [x[i].varValue for i in range(T + 1)]
velocities = [v[i].varValue for i in range(T + 1)]
accelerations = [a[i].varValue for i in range(T)]

# Total fuel spent
fuel_spent = pulp.value(problem.objective)

# Printing Output
print(f'Positions: {positions}')
print(f'Velocities: {velocities}')
print(f'Accelarations: {accelerations}')
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')