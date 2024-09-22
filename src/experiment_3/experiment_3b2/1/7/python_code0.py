import pulp

# Given data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)       # Acceleration
M = pulp.LpVariable("M", lowBound=0)                          # Maximum thrust

# Objective function
problem += M

# Initial conditions
problem += (x[0] == x0, "Initial_Position")
problem += (v[0] == v0, "Initial_Velocity")

# Target conditions
problem += (x[T] == xT, "Final_Position")
problem += (v[T] == vT, "Final_Velocity")

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

    # Constraints on acceleration
    problem += (a[t] <= M, f"Max_Thrust_Upper_{t}")
    problem += (a[t] >= -M, f"Max_Thrust_Lower_{t}")

# Objective Value Print
problem.solve()

# Output information
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]

total_fuel_spend = sum(abs(a[t].varValue) for t in range(T))

# Print output
print(f'Positions: {positions}')
print(f'Velocities: {velocities}')
print(f'Accelerations: {accelerations}')
print(f'Total Fuel Spend: {total_fuel_spend}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')