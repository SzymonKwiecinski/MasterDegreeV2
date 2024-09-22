import pulp

# Parse JSON data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Parameters
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create a LP minimization problem
problem = pulp.LpProblem("Rocket_Path_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T))
M = pulp.LpVariable("M", lowBound=0)

# Objective Function: Minimize maximum thrust required
problem += M, "Minimize_Maximum_Thrust"

# Constraints

# Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

# Final conditions
problem += (x[T] == XT, "Final_Position")
problem += (v[T] == VT, "Final_Velocity")

# Dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")
    problem += (-M <= a[t], f"Negative_Thrust_Bound_{t}")
    problem += (a[t] <= M, f"Positive_Thrust_Bound_{t}")

# Solve the problem
problem.solve()

# Get the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')