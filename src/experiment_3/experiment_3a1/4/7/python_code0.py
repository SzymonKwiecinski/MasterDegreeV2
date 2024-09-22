import pulp

# Data extraction from the provided JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Create the linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Define decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity

# Set initial conditions
x[0] = X0
v[0] = V0

# Objective function to minimize maximum acceleration (thrust)
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

# Constraints for each time step
for t in range(T):
    # Position and velocity update equations
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    
    # Constrain max thrust
    problem += a[t] <= max_thrust
    problem += -a[t] <= max_thrust

# Constraints for reaching target position and velocity
problem += x[T] == XT
problem += v[T] == VT

# Solve the problem
problem.solve()

# Collect results
result_x = [pulp.value(x[t]) for t in range(T + 1)]
result_v = [pulp.value(v[t]) for t in range(T + 1)]
result_a = [pulp.value(a[t]) for t in range(T)]

# Total fuel spent
fuel_spend = pulp.value(problem.objective)

# Output summary
print(f'Output:')
print(f'{"x"}: {result_x}')
print(f'{"v"}: {result_v}')
print(f'{"a"}: {result_a}')
print(f'{"fuel_spend"}: {fuel_spend}')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')