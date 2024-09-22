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
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: minimize the maximum thrust (acceleration)
max_a = pulp.LpVariable("max_a", lowBound=0)
problem += max_a

# Constraints
problem += (x[0] == x_0)
problem += (v[0] == v_0)

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])
    problem += (a[t] <= max_a)
    problem += (a[t] >= -max_a)

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "x": [pulp.value(x[t]) for t in range(T + 1)],
    "v": [pulp.value(v[t]) for t in range(T + 1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(max_a)
}

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the output
print(json.dumps(output, indent=4))