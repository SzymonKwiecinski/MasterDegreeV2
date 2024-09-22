import pulp

# Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Thrust_Minimization", pulp.LpMinimize)

# Define the variables
M = pulp.LpVariable("M", lowBound=0)  # Maximum thrust
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=-M, upBound=M)

# Initial conditions
x[0] = X0
v[0] = V0

# Objective Function
problem += M, "Minimize_Maximum_Thrust"

# Constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"

# Final conditions
problem += x[T] == XT, "Final_Position_Constraint"
problem += v[T] == VT, "Final_Velocity_Constraint"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')