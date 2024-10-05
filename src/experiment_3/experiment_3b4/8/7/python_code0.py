import pulp

# Load data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Initialize problem
problem = pulp.LpProblem("Rocket_Landing_Optimization", pulp.LpMinimize)

# Define variables
x = pulp.LpVariable.dicts("x", range(data['T'] + 1))
v = pulp.LpVariable.dicts("v", range(data['T'] + 1))
a = pulp.LpVariable.dicts("a", range(data['T']), lowBound=None)
M = pulp.LpVariable("M", lowBound=0)

# Objective Function
problem += M

# Constraints
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t]), f"Position_Constraint_{t}"
    problem += (v[t + 1] == v[t] + a[t]), f"Velocity_Constraint_{t}"
    problem += (a[t] <= M), f"Max_Thrust_Constraint_Pos_{t}"
    problem += (a[t] >= -M), f"Max_Thrust_Constraint_Neg_{t}"

# Initial conditions
problem += (x[0] == data['X0']), "Initial_Position"
problem += (v[0] == data['V0']), "Initial_Velocity"

# Final conditions
problem += (x[data['T']] == data['XT']), "Final_Position"
problem += (v[data['T']] == data['VT']), "Final_Velocity"

# Solve problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')