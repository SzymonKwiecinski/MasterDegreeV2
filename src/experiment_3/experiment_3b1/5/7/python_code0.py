import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T + 1)]
max_a = pulp.LpVariable("max_a", lowBound=0)

# Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

# Dynamic equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Target conditions
problem += (x[T] == xT)
problem += (v[T] == vT)

# Objective: Minimize the maximum thrust required
for t in range(T + 1):
    problem += (max_a >= a[t])

problem += pulp.lpSum([max_a])  # Minimize max_a

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')