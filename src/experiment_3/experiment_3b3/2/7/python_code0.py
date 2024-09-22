import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Unpack data
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]
max_thrust = pulp.LpVariable('max_thrust', lowBound=0, cat='Continuous')

# Objective
problem += max_thrust

# Initial and final conditions
problem += (x[0] == x0)
problem += (v[0] == v0)
problem += (x[T] == xT)
problem += (v[T] == vT)

# Dynamical equations and thrust constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (a[t] <= max_thrust)
    problem += (-a[t] <= max_thrust)

# Solve
problem.solve()

# Calculate fuel spent
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

# Collect results
result = {
    'x': [pulp.value(x[t]) for t in range(T + 1)],
    'v': [pulp.value(v[t]) for t in range(T + 1)],
    'a': [pulp.value(a[t]) for t in range(T)],
    'fuel_spend': fuel_spent,
}

# Output
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')