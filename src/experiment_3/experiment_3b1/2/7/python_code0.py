import pulp

# Input data from JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # Acceleration variables
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)   # Max thrust variable

# Objective function: Minimize the maximum thrust
problem += max_thrust, "MinimizeMaxThrust"

# Constraints for the rocket motion model
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]

# Initial conditions
problem += (x[0] == X0, "InitialPosition")
problem += (v[0] == V0, "InitialVelocity")

# Evolution constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionEvolution_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityEvolution_{t}")

# Final conditions
problem += (x[T] == XT, "TargetPosition")
problem += (v[T] == VT, "TargetVelocity")

# Maximum thrust constraint
for t in range(T):
    problem += (a[t] <= max_thrust, f"MaxThrustConstraintPos_{t}")
    problem += (a[t] >= -max_thrust, f"MaxThrustConstraintNeg_{t}")

# Solve the problem
problem.solve()

# Output results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("Positions:", positions)
print("Velocities:", velocities)
print("Accelerations:", accelerations)
print("Total Fuel Spent:", fuel_spent)