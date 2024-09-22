import pulp

# Data from the JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

# Objective variable: maximum absolute acceleration
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)

# Objective function: minimize the maximum thrust
problem += max_thrust

# Constraints
problem += x[0] == x0
problem += v[0] == v0
problem += x[T] == xT
problem += v[T] == vT

# Dynamics constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    
# Maximum thrust constraints
for t in range(T):
    problem += a[t] <= max_thrust
    problem += -a[t] <= max_thrust

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')