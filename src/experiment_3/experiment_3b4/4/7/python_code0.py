import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]
u = pulp.LpVariable("u", lowBound=0, cat='Continuous')

# Objective
problem += u, "Minimize_maximum_thrust"

# Constraints

# Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

# Target conditions
problem += (x[T] == XT, "Target_Position")
problem += (v[T] == VT, "Target_Velocity")

# Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Dynamics_Position_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Dynamics_Velocity_{t}")

# Absolute value linearization
for t in range(T):
    problem += (a[t] <= u, f"Abs_Upper_{t}")
    problem += (-a[t] <= u, f"Abs_Lower_{t}")

# Solve
problem.solve()

# Print Results
positions = [x[t].varValue for t in range(T+1)]
velocities = [v[t].varValue for t in range(T+1)]
accelerations = [a[t].varValue for t in range(T)]
fuel_spend = sum(abs(a[t].varValue) for t in range(T))

print(f"Positions: {positions}")
print(f"Velocities: {velocities}")
print(f"Accelerations: {accelerations}")
print(f"Fuel Spend: {fuel_spend}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')