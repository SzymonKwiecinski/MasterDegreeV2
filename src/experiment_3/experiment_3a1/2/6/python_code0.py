import pulp

# Data dictionary
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Extract data
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # Acceleration
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)  # Position
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)  # Velocity

# Initial conditions
problem += (x[0] == x0, "InitialPosition")
problem += (v[0] == v0, "InitialVelocity")

# Objective function: minimize total fuel consumption (total acceleration)
problem += pulp.lpSum(pulp.abs(a[t]) for t in range(T)), "TotalFuelConsumption"

# Constraints for motion
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"PositionConstraint_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"VelocityConstraint_{t}"

# Final conditions
problem += (x[T] == xT, "FinalPosition")
problem += (v[T] == vT, "FinalVelocity")

# Solve the problem
problem.solve()

# Collect the results
positions = [pulp.value(x[t]) for t in range(T+1)]
velocities = [pulp.value(v[t]) for t in range(T+1)]
accelerations = [pulp.value(a[t]) for t in range(T)]

# Total fuel spent
total_fuel = pulp.value(problem.objective)

# Output the results
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": total_fuel
}

print(f' (Objective Value): <OBJ>{total_fuel}</OBJ>')