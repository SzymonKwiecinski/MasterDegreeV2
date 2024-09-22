import pulp
import json

# Input data in JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extracting values from the input data
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=-pulp.LpInfinity, upBound=pulp.LpInfinity) for t in range(T)]

# Objective function: minimize the maximum thrust
max_thrust = pulp.LpVariable('max_thrust', lowBound=0)
problem += max_thrust

# Constraints
problem += (x[0] == x_0)
problem += (v[0] == v_0)

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])
    problem += (a[t] <= max_thrust)
    problem += (a[t] >= -max_thrust)

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Solve the problem
problem.solve()

# Preparing the output
result = {
    "x": [pulp.value(x[t]) for t in range(T + 1)],
    "v": [pulp.value(v[t]) for t in range(T + 1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(max_thrust)
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Printing the final results
print(json.dumps(result))