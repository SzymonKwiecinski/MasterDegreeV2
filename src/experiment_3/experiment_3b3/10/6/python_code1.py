import pulp

# Data from JSON
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Model parameters
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create a problem instance
problem = pulp.LpProblem("RocketMotionOptimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

# Objective function
problem += pulp.lpSum([pulp.lpSum([a[t], -a[t]]) for t in range(T)])  # Using the absolute value via sum of two variables

# Initial condition constraints
problem += (x[0] == x0, "Initial_Position")
problem += (v[0] == v0, "Initial_Velocity")

# State transition constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Transition_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Transition_{t}")

# Terminal condition constraints
problem += (x[T] == xT, "Final_Position")
problem += (v[T] == vT, "Final_Velocity")

# Solve the problem
problem.solve()

# Extracting results
position = [pulp.value(x[t]) for t in range(T+1)]
velocity = [pulp.value(v[t]) for t in range(T+1)]
acceleration = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

# Print the results
result = {
    "x": position,
    "v": velocity,
    "a": acceleration,
    "fuel_spend": fuel_spent
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')