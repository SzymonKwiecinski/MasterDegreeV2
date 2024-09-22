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
problem = pulp.LpProblem("Rocket_Fuel_Optimization", pulp.LpMinimize)

# Create variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: minimize fuel usage
problem += pulp.lpSum([pulp.lpSum([a[t] for t in range(T)])])

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Dynamic constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Final condition
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Solve the problem
problem.solve()

# Prepare output
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Output data
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

# Print objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')