import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the linear programming problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective: Minimize the maximum thrust (acceleration)
max_a = pulp.LpVariable("max_a", lowBound=0)
problem += max_a

# Constraints for position and velocity update equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]

# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

# Constraints for acceleration and its maximum
for t in range(T):
    problem += a[t] <= max_a
    problem += a[t] >= -max_a

# Solve the problem
problem.solve()

# Collect outputs
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_a)

# Prepare output data
output = {
    "x": positions[1:],  # Exclude initial position
    "v": velocities[1:],  # Exclude initial velocity
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')