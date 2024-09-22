import pulp

# Problem data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 
        'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create a linear programming problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum([pulp.lpSum([pulp.lpSum([pulp.lpSum([pulp.abs(a[t])])])]) for t in range(T)])

# Initial conditions
problem += (x[0] == x_0, "InitialPosition")
problem += (v[0] == v_0, "InitialVelocity")

# Target constraints
problem += (x[T] == x_T, "FinalPosition")
problem += (v[T] == v_T, "FinalVelocity")

# Dynamic constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"DynamicPosition_{t}")
    problem += (v[t+1] == v[t] + a[t], f"DynamicVelocity_{t}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')