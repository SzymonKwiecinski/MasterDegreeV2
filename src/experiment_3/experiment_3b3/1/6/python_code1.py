import pulp
import json

# Load data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Extract data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]

# Define the objective function
problem += pulp.lpSum([pulp.lpSum([a[t], -a[t]]) for t in range(T)])  # Using absolute values manually

# Add initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Add final conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Add motion dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")

# Solve the problem
problem.solve()

# Extract the values
x_values = [pulp.value(var) for var in x]
v_values = [pulp.value(var) for var in v]
a_values = [pulp.value(var) for var in a]
fuel_spent = pulp.value(problem.objective)

# Output result
result = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}

# Print the objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')

# For inspection
print(json.dumps(result, indent=4))