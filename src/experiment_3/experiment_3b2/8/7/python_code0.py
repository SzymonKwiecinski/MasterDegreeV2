import pulp

# Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']
M = 10  # Define a large finite value for M

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Fuel_Spend", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=-M, upBound=M)

# Objective Function
problem += pulp.lpSum(a[t] for t in range(T)), "Total_Fuel_Spend"

# Initial Conditions
problem += x[0] == X0, "Initial_Position"
problem += v[0] == V0, "Initial_Velocity"
problem += x[T] == XT, "Final_Position"
problem += v[T] == VT, "Final_Velocity"

# Dynamics Constraints
for t in range(T - 1):
    problem += x[t + 1] == x[t] + v[t], f"Position_Update_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')