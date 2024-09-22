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
problem = pulp.LpProblem("Rocket_Acceleration_Problem", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T + 1)]
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)

# Initialize the rocket's position and velocity
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Constraints for the dynamics
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])
    problem += (max_thrust >= a[t])  # |a_t| <= max_thrust
    problem += (max_thrust >= -a[t])  # -|a_t| <= max_thrust

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Objective function
problem += max_thrust  # Minimize the maximum thrust required

# Solve the problem
problem.solve()

# Collect results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T + 1)]
fuel_spent = pulp.value(max_thrust)

# Format output
result = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Print results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')