import pulp
import json

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Extracting values from the data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the problem
problem = pulp.LpProblem("RocketFuelMinimization", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # accelerations
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # positions
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocities

# Objective function: Minimize total fuel consumption
problem += pulp.lpSum(a[t] if a[t] >= 0 else -a[t] for t in range(T)), "TotalFuel"

# Initial conditions
problem += x[0] == x_0, "InitialPosition"
problem += v[0] == v_0, "InitialVelocity"

# State update equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionUpdate_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityUpdate_{t}"

# Final conditions
problem += x[T] == x_T, "FinalPosition"
problem += v[T] == v_T, "FinalVelocity"

# Solve the problem
problem.solve()

# Prepare output
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Output result
result = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')