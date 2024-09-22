import pulp

# Load data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Motion", pulp.LpMinimize)

# Define variables
M = pulp.LpVariable("M", lowBound=0)  # Maximum thrust
a = [pulp.LpVariable(f'a_{t}', lowBound=-M, upBound=M) for t in range(T + 1)]  # Acceleration at each time step
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]  # Position at each time step
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]  # Velocity at each time step

# Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

# State update equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")

# Final conditions
problem += (x[T] == XT, "Final_Position")
problem += (v[T] == VT, "Final_Velocity")

# Maximum thrust constraints
for t in range(T + 1):
    problem += (M >= pulp.lpSum([a[t]]), f"Max_Thrust_Constraint_{t}")

# Objective function
problem += M  # Minimize the maximum thrust

# Solve the problem
problem.solve()

# Output results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T + 1)]
fuel_spend = pulp.value(M) * (T + 1)  # This can be defined based on specific fuel consumption logic.

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Positions: {x_values}')
print(f'Velocities: {v_values}')
print(f'Accelerations: {a_values}')
print(f'Total Fuel Spent: {fuel_spend}')