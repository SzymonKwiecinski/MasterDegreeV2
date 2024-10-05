import pulp

# Extract data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create a LP problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')

# Objective
problem += M, "Minimize_Maximum_Thrust"

# Constraints

# Initial Conditions
problem += (x[0] == X0), "Initial_Position"
problem += (v[0] == V0), "Initial_Velocity"

# Target Conditions
problem += (x[T] == XT), "Target_Position"
problem += (v[T] == VT), "Target_Velocity"

# Position and Velocity Constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"Position_Constraint_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"Velocity_Constraint_{t}"

# Thrust Constraints
for t in range(T):
    problem += (-M <= a[t]), f"Thrust_Lower_Bound_{t}"
    problem += (a[t] <= M), f"Thrust_Upper_Bound_{t}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')