import pulp

# Given data from JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Define decision variables
M = pulp.LpVariable("M", lowBound=0)  # Maximum absolute acceleration
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # Acceleration at each time step
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Position at each time step
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocity at each time step

# Objective function: minimize M
problem += M, "Minimize_Max_Acceleration"

# Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

# Constraints for position and velocity
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

    # Constraints on acceleration
    problem += (a[t] <= M, f"Max_Acceleration_{t}")
    problem += (-a[t] <= M, f"Min_Acceleration_{t}")

# Final conditions
problem += (x[T] == XT, "Final_Position")
problem += (v[T] == VT, "Final_Velocity")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')