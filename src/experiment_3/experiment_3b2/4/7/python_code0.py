import pulp
import json

# Data provided in JSON format
data = json.loads("{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}")
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Initialize the problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Positions
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocities
a = pulp.LpVariable.dicts("a", range(T + 1), lowBound=None)  # Accelerations
M = pulp.LpVariable("M", lowBound=None)  # Maximum acceleration

# Objective function: Minimize M
problem += M, "Minimize_Max_Thrust"

# Constraints
problem += x[0] == X0, "Initial_Position"
problem += v[0] == V0, "Initial_Velocity"
problem += x[T] == XT, "Final_Position"
problem += v[T] == VT, "Final_Velocity"

# State transition constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"

# Acceleration limits
for t in range(T + 1):
    problem += a[t] <= M, f"Max_Acceleration_{t}"
    problem += -a[t] <= M, f"Min_Acceleration_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')