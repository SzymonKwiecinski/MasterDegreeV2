import pulp

# Data from the provided JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Extract parameters
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Motion_Problem", pulp.LpMinimize)

# Variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity

# Objective function: Minimize the total fuel used (sum of absolute values of accelerations)
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)]), "MinimizeFuel"

# Constraints
# Initial conditions
problem += x[0] == x0, "InitialPosition"
problem += v[0] == v0, "InitialVelocity"

# Dynamics
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionDynamics_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityDynamics_{t}"

# Target conditions
problem += x[T] == xT, "FinalPosition"
problem += v[T] == vT, "FinalVelocity"

# Solve the problem
problem.solve()

# Collect results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spend = pulp.value(problem.objective)

# Output the results
result = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spend
}

print(f' (Objective Value): <OBJ>{fuel_spend}</OBJ>')