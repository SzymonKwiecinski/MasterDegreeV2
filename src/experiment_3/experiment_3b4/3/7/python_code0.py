import pulp

# Problem data
data = {
    'X0': 0,
    'V0': 0,
    'XT': 1,
    'VT': 0,
    'T': 20
}

# Create the LP problem
problem = pulp.LpProblem("Rocket_Minimum_Thrust", pulp.LpMinimize)

# Variables
x = {t: pulp.LpVariable(f"x_{t}") for t in range(data['T'] + 1)}
v = {t: pulp.LpVariable(f"v_{t}") for t in range(data['T'] + 1)}
a = {t: pulp.LpVariable(f"a_{t}", lowBound=None) for t in range(data['T'])}
M = pulp.LpVariable("M", lowBound=0)

# Objective
problem += M, "Minimize_Maximum_Acceleration"

# Constraints
# Initial conditions
problem += x[0] == data['X0'], "Initial_Position"
problem += v[0] == data['V0'], "Initial_Velocity"

# Dynamics over time
for t in range(data['T']):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"
    problem += a[t] <= M, f"Acceleration_Positive_Constraint_{t}"
    problem += -a[t] <= M, f"Acceleration_Negative_Constraint_{t}"

# Final conditions
problem += x[data['T']] == data['XT'], "Final_Position"
problem += v[data['T']] == data['VT'], "Final_Velocity"

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')