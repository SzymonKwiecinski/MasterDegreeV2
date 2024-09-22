import pulp

# Given data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Define problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Time horizon
T = data['T']

# Decision Variables
x = pulp.LpVariable.dicts("Position", range(T + 1), cat='Continuous')
v = pulp.LpVariable.dicts("Velocity", range(T + 1), cat='Continuous')
a = pulp.LpVariable.dicts("Acceleration", range(T), cat='Continuous')
z = pulp.LpVariable("Max_Absolute_Acceleration", lowBound=0, cat='Continuous')

# Objective Function: Minimize the maximum absolute acceleration
problem += z

# Initial conditions
problem += (x[0] == data['X0'], "Initial_Position")
problem += (v[0] == data['V0'], "Initial_Velocity")

# Target conditions
problem += (x[T] == data['XT'], "Target_Position")
problem += (v[T] == data['VT'], "Target_Velocity")

# Equations for position and velocity
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")

# Constraints on acceleration to minimize max absolute value
for t in range(T):
    problem += (-z <= a[t], f"Accel_Lower_Bound_{t}")
    problem += (a[t] <= z, f"Accel_Upper_Bound_{t}")

# Solve the problem
problem.solve()

# Print the objective value (minimized maximum absolute acceleration)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')