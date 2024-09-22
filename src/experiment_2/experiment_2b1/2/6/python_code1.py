import pulp
import json

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the linear programming problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Define decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: minimize total fuel spent
fuel_spent = pulp.lpSum([a[t] for t in range(T)])  # Since a[t] should be non-negative, we do not need abs
problem += fuel_spent, "TotalFuel"

# Initial conditions
problem += (x[0] == x_0, "InitialPosition")
problem += (v[0] == v_0, "InitialVelocity")

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionDynamics_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityDynamics_{t}")

# Terminal conditions
problem += (x[T] == x_T, "FinalPosition")
problem += (v[T] == v_T, "FinalVelocity")

# Solve the problem
problem.solve()

# Prepare results
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]
fuel_spent_value = pulp.value(problem.objective)

# Output the results
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent_value,
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{fuel_spent_value}</OBJ>')