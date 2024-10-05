import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Problem
problem = pulp.LpProblem("Rocket_Trajectory_Control", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')

# Objective
problem += M

# Constraints
# Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

# Target conditions
problem += (x[T] == XT, "Target_Position")
problem += (v[T] == VT, "Target_Velocity")

# Dynamics
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")

# Maximum thrust constraint
for t in range(T):
    problem += (-M <= a[t], f"Max_Thrust_Lower_{t}")
    problem += (a[t] <= M, f"Max_Thrust_Upper_{t}")

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')