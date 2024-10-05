import pulp

# Data from the problem statement
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Path_Optimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("position", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("velocity", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("acceleration", range(T), lowBound=-pulp.LpInfinity, upBound=pulp.LpInfinity)
M = pulp.LpVariable("M", lowBound=0)

# Objective function
problem += M

# Constraints
problem += x[0] == X0  # Initial position
problem += v[0] == V0  # Initial velocity
problem += x[T] == XT  # Target position
problem += v[T] == VT  # Target velocity

# Dynamics constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]  # Position update
    problem += v[t + 1] == v[t] + a[t]  # Velocity update
    problem += a[t] <= M  # Acceleration constraint
    problem += a[t] >= -M  # Acceleration constraint

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')