import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Parameters
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: Minimize the maximum thrust required
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust, "Objective"

# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Dynamics constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"
    problem += a[t] <= max_thrust, f"Thrust_Upper_Bound_{t}"
    problem += a[t] >= -max_thrust, f"Thrust_Lower_Bound_{t}"

# Final conditions
problem += x[T] == x_T, "Final_Position"
problem += v[T] == v_T, "Final_Velocity"

# Solve the problem
problem.solve()

# Collect results
results = {
    "x": [pulp.value(x[t]) for t in range(T + 1)],
    "v": [pulp.value(v[t]) for t in range(T + 1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(max_thrust)
}

# Print the results
print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')