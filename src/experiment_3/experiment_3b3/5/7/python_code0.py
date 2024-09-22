import pulp

# Data
data = {
    'X0': 0,
    'V0': 0,
    'XT': 1,
    'VT': 0,
    'T': 20
}

# Extract parameters
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Define Linear Programming problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
max_thrust = pulp.LpVariable("max_thrust", lowBound=0, cat='Continuous')

# Objective function: Minimize maximum thrust
problem += max_thrust

# Initial conditions
problem += (x[0] == x0, "Initial_Position")
problem += (v[0] == v0, "Initial_Velocity")

# Final conditions
problem += (x[T] == xT, "Final_Position")
problem += (v[T] == vT, "Final_Velocity")

# Model equations and max thrust constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Equation_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Equation_{t}")
    problem += (max_thrust >= a[t], f"Max_Thrust_Pos_{t}")
    problem += (max_thrust >= -a[t], f"Max_Thrust_Neg_{t}")

# Solve the problem
problem.solve()

# Results
result_x = [pulp.value(x[t]) for t in range(T + 1)]
result_v = [pulp.value(v[t]) for t in range(T + 1)]
result_a = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

output = {
    "x": result_x,
    "v": result_v,
    "a": result_a,
    "fuel_spent": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')