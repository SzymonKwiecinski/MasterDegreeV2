import pulp
import json

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: Minimize total fuel consumption (sum of absolute accelerations)
problem += pulp.lpSum([pulp.lpSum([a[t]]) for t in range(T)])

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Constraints for the rocket's motion
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Solve the problem
problem.solve()

# Gather results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]

# Calculate total fuel spent
fuel_spent = pulp.value(problem.objective)

# Prepare output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Output the objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')