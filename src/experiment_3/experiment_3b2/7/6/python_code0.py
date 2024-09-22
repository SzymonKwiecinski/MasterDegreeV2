import pulp

# Data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Problem definition
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]
u = [pulp.LpVariable(f'u_{t}', lowBound=0) for t in range(T)]

# Objective Function
problem += pulp.lpSum(u[t] for t in range(T))

# Initial Conditions
problem += x[0] == x0
problem += v[0] == v0

# Final Conditions
problem += x[T] == xT
problem += v[T] == vT

# Dynamic Constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += u[t] >= a[t]  # Ensuring u_t >= a_t
    problem += u[t] >= -a[t] # Ensuring u_t >= -a_t

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')