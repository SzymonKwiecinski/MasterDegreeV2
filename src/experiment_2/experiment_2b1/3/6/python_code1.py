import pulp
import json

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the problem
problem = pulp.LpProblem("Rocket_Control", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Objective function: Minimize fuel usage
problem += pulp.lpSum([pulp.LpVariable(f'abs_a_{t}', lowBound=0) for t in range(T)])  # Create auxiliary variables for absolute values
for t in range(T):
    problem += (pulp.LpVariable(f'abs_a_{t}') == a[t])  # Link auxiliary variable to acceleration variable

# Solve the problem
problem.solve()

# Collect results
fuel_spent = pulp.value(problem.objective)
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]

# Prepare output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')