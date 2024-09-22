import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_LP", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]
max_a = pulp.LpVariable("max_a", lowBound=0)

# Objective function: Minimize the maximum thrust required
problem += max_a

# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Constraints for the rocket motion
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += a[t] <= max_a
    problem += a[t] >= -max_a

# Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

# Solve the problem
problem.solve()

# Extracting results
x_result = [pulp.value(x[t]) for t in range(T + 1)]
v_result = [pulp.value(v[t]) for t in range(T + 1)]
a_result = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_a) * T  # using max_a as fuel consumption per time unit

# Prepare the output
output = {
    "x": x_result,
    "v": v_result,
    "a": a_result,
    "fuel_spend": fuel_spent,
}

# Print the output
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')