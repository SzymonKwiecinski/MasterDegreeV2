import pulp

# Parse the input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Define problem
problem = pulp.LpProblem("Minimize_Absolute_Acceleration", pulp.LpMinimize)

# Time steps
T = data['TotalTime']

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, cat='Continuous')
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)])

# Initial conditions
problem += x[0] == data['InitialPosition']
problem += v[0] == data['InitialVelocity']

# Final conditions
problem += x[T] == data['FinalPosition']
problem += v[T] == data['FinalVelocity']

# Constraints
for t in range(T):
    problem += x[t+1] == x[t] + v[t]
    problem += v[t+1] == v[t] + a[t]

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')