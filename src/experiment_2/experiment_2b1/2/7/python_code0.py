import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Thrust_Optimization", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# End conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Objective: minimize the maximum thrust (acceleration)
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
for t in range(T):
    problem += (a[t] <= max_thrust)
    problem += (a[t] >= -max_thrust)

problem += max_thrust

# Solve the problem
problem.solve()

# Prepare output
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_thrust) * T  # assuming fuel spent is max thrust over time

# Output result
result = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')