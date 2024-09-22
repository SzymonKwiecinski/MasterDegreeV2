import pulp

# Data from JSON format
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Model parameters
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # Acceleration at each time step
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)  # Position at each time step
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)  # Velocity at each time step

# Objective function: Minimize total fuel cost
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)]), "Total_Fuel_Cost"

# Constraints

# Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

# Dynamics
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

# Final conditions
problem += (x[T] == x_T, "Final_Position_Condition")
problem += (v[T] == v_T, "Final_Velocity_Condition")

# Solve the problem
problem.solve()

# Output the results
output = {
    "x": [x[t].varValue for t in range(T + 1)],
    "v": [v[t].varValue for t in range(T + 1)],
    "a": [a[t].varValue for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>') 