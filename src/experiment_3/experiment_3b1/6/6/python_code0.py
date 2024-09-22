import pulp

# Given data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create the optimization problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Define decision variables
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]  # Acceleration variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T)]  # Position variables
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T)]  # Velocity variables

# Objective function: Minimize the total fuel spent
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)]), "TotalFuelSpent"

# Constraints
# Initial conditions
problem += (x[0] == x0, "InitialPosition")
problem += (v[0] == v0, "InitialVelocity")

# Relationships for each time step
for t in range(T - 1):
    problem += (x[t + 1] == x[t] + v[t], f"PositionUpdate_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityUpdate_{t}")

# Final conditions
problem += (x[T - 1] == xT, "FinalPosition")
problem += (v[T - 1] == vT, "FinalVelocity")

# Solve the problem
problem.solve()

# Collect results
result = {
    "x": [pulp.value(x[t]) for t in range(T)],
    "v": [pulp.value(v[t]) for t in range(T)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')