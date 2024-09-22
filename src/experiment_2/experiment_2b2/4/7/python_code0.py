import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Problem definition
problem = pulp.LpProblem("Minimum_Thrust_Rocket", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(data['T'] + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(data['T'] + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(data['T'] + 1)]
thrust = pulp.LpVariable("max_thrust", lowBound=0, cat='Continuous')

# Objective function: Minimize maximum thrust
problem += thrust

# Initial conditions
problem += (x[0] == data['X0'], "Initial_Position")
problem += (v[0] == data['V0'], "Initial_Velocity")

# Dynamics constraints
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")

# Final conditions
problem += (x[data['T']] == data['XT'], "Target_Position")
problem += (v[data['T']] == data['VT'], "Target_Velocity")

# Thrust constraints
for t in range(data['T']):
    problem += (a[t] <= thrust, f"Thrust_Upper_{t}")
    problem += (a[t] >= -thrust, f"Thrust_Lower_{t}")

# Solve the problem
problem.solve()

# Output results
positions = [pulp.value(x[t]) for t in range(1, data['T'] + 1)]
velocities = [pulp.value(v[t]) for t in range(1, data['T'] + 1)]
accelerations = [pulp.value(a[t]) for t in range(1, data['T'] + 1)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(data['T']))

output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
print(output)