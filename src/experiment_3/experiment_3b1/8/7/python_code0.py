import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Define decision variables
a = pulp.LpVariable.dicts("a", range(T + 1), lowBound=None)
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
Z = pulp.LpVariable("Z", lowBound=0)

# Objective Function: Minimize the maximum absolute acceleration
problem += Z

# Constraints
# Initial conditions
problem += x[0] == X0
problem += v[0] == V0

# Dynamics and thrust constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += -Z <= a[t]
    problem += a[t] <= Z

# Final conditions
problem += x[T] == XT
problem += v[T] == VT

# Solve the problem
problem.solve()

# Output results
for t in range(T + 1):
    print(f"x[{t}]: {x[t].varValue}, v[{t}]: {v[t].varValue}, a[{t}]: {a[t].varValue}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')