import pulp
import json

# Load the data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Extract variables from data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Problem", pulp.LpMinimize)

# Create variables for position, velocity, and acceleration
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: Minimize total fuel spent
problem += pulp.lpSum(abs(a[t]) for t in range(T)), "TotalFuel"

# Initial Conditions
problem += (x[0] == x_0), "InitialPosition"
problem += (v[0] == v_0), "InitialVelocity"

# Constraints for the rocket's motion
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t]), f"PositionConstraint_{t}"
    problem += (v[t + 1] == v[t] + a[t]), f"VelocityConstraint_{t}"

# Final Conditions
problem += (x[T] == x_T), "FinalPosition"
problem += (v[T] == v_T), "FinalVelocity"

# Solve the problem
problem.solve()

# Extract results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Prepare output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')