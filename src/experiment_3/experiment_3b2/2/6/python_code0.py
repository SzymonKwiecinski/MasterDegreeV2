import pulp

# Given data
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Parameters
T = data['TotalTime']
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']

# Create the linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=None) for t in range(T)]

# Objective function
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)]), "TotalFuelConsumption"

# Initial conditions
problem += (x[0] == x0, "InitialPosition")
problem += (v[0] == v0, "InitialVelocity")

# Dynamics
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionDynamics_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityDynamics_{t}")

# Target conditions
problem += (x[T] == xT, "FinalPosition")
problem += (v[T] == vT, "FinalVelocity")

# Absolute value constraints
for t in range(T):
    problem += (a[t] >= 0, f"AccelerationPositive_{t}")
    problem += (a[t] <= pulp.lpSum([a[t]]), f"AccelerationNegative_{t}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')