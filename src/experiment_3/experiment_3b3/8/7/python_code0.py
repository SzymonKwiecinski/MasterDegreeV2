import pulp

# Load data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)
M = pulp.LpVariable("M", lowBound=0)

# Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

# Terminal conditions
problem += (x[T] == xT)
problem += (v[T] == vT)

# Constraints and dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (a[t] >= -M)
    problem += (a[t] <= M)

# Objective
problem += M

# Solve the problem
problem.solve()

# Extract solution and output results
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spend = sum(abs(a_val) for a_val in a_values)

# Display the results
print(f"x = {x_values}")
print(f"v = {v_values}")
print(f"a = {a_values}")
print(f"fuel_spend = {fuel_spend}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')