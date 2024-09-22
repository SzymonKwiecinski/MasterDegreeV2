import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("RocketMotionOptimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]

# Objective function: minimize maximum thrust (acceleration)
max_thrust = pulp.LpVariable('max_thrust', lowBound=0)
problem += max_thrust

# Constraints
problem += x[0] == x0
problem += v[0] == v0
problem += x[T] == xT
problem += v[T] == vT

# Motion equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += a[t] <= max_thrust
    problem += a[t] >= -max_thrust

# Solve the problem
problem.solve()

# Collect results
x_sol = [pulp.value(x[t]) for t in range(T + 1)]
v_sol = [pulp.value(v[t]) for t in range(T + 1)]
a_sol = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_thrust)

# Output the results in the specified format
output = {
    "x": x_sol,
    "v": v_sol,
    "a": a_sol,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')