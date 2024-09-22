import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Define variables
M = pulp.LpVariable("M", lowBound=0)
a = pulp.LpVariable.dicts("a", range(T-1), lowBound=None)  # Acceleration
x = pulp.LpVariable.dicts("x", range(T), lowBound=None)  # Position
v = pulp.LpVariable.dicts("v", range(T), lowBound=None)  # Velocity

# Objective function
problem += M  # Minimize the maximum thrust

# Constraints
problem += x[0] == x_0  # Initial position constraint
problem += v[0] == v_0  # Initial velocity constraint

for t in range(T-1):
    problem += x[t + 1] == x[t] + v[t]  # Position update
    problem += v[t + 1] == v[t] + a[t]  # Velocity update
    problem += -M <= a[t]  # Lower bound on acceleration
    problem += a[t] <= M  # Upper bound on acceleration

# Final conditions
problem += x[T-1] == x_T  # Final position constraint
problem += v[T-1] == v_T  # Final velocity constraint

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')