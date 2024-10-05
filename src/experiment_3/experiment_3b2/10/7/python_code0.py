import pulp

# Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Acceleration_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Position", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("Velocity", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("Acceleration", range(T), lowBound=None)
M = pulp.LpVariable("M", lowBound=0)

# Objective Function
problem += M

# Initial Conditions
problem += x[0] == X0
problem += v[0] == V0

# Final Conditions
problem += x[T] == XT
problem += v[T] == VT

# Dynamics Constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]

# Acceleration Bounds
for t in range(T):
    problem += -M <= a[t]
    problem += a[t] <= M

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')