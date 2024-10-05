import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Variables
T = data['T']
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=-pulp.lpSum([1]), upBound=pulp.lpSum([1]), cat='Continuous') for t in range(T)]
max_thrust = pulp.LpVariable('max_thrust', lowBound=0, cat='Continuous')

# Objective
problem += max_thrust

# Constraints
problem += (x[0] == data['X0'])
problem += (v[0] == data['V0'])

for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (max_thrust >= pulp.lpSum([a[t]]))
    problem += (max_thrust >= -pulp.lpSum([a[t]]))

# Final Condition Constraints
problem += (x[T] == data['XT'])
problem += (v[T] == data['VT'])

# Solve
problem.solve()

# Output
outputs = {
    'x': [pulp.value(x[t]) for t in range(T+1)],
    'v': [pulp.value(v[t]) for t in range(T+1)],
    'a': [pulp.value(a[t]) for t in range(T)],
    'fuel_spend': pulp.value(sum([pulp.lpSum([abs(a[t])]) for t in range(T)]))
}

print(outputs)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')