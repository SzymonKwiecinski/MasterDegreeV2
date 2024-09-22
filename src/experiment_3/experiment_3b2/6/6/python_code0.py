import pulp

# Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Variables
T = data['TotalTime']
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)
u = pulp.LpVariable.dicts("u", range(T), lowBound=0)

# Problem
problem = pulp.LpProblem("MinimizeAcceleration", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum(u[t] for t in range(T))

# Constraints
problem += (x[0] == data['InitialPosition'])
problem += (v[0] == data['InitialVelocity'])

for t in range(T-1):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (u[t] >= a[t])
    problem += (u[t] >= -a[t])

problem += (x[T] == data['FinalPosition'])
problem += (v[T] == data['FinalVelocity'])

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')