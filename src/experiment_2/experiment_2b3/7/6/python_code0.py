import pulp

# Data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data["InitialPosition"]
v_0 = data["InitialVelocity"]
x_T = data["FinalPosition"]
v_T = data["FinalVelocity"]
T = data["TotalTime"]

# Problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

# Objective function: Minimize fuel consumption
problem += pulp.lpSum([pulp.lpSum([
    pulp.lpSum([a_t, -a_t]) for a_t in a
])])

# Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Final conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")

# Solve the problem
problem.solve()

# Extracting results
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(a_t) for a_t in a_values)

# Output format
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')