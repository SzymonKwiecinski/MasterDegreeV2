import pulp

# Data
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Extract data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Initialize the LP problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Create variables for position, velocity, and acceleration
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T+1)]
a_plus = [pulp.LpVariable(f'a_plus_{t}', lowBound=0, cat='Continuous') for t in range(T)]
a_minus = [pulp.LpVariable(f'a_minus_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective function: Minimize total fuel consumption
problem += pulp.lpSum(a_plus[t] + a_minus[t] for t in range(T))

# Initial conditions
problem += x[0] == x_0, "Initial_Position"
problem += v[0] == v_0, "Initial_Velocity"

# Motion equations
for t in range(T):
    problem += x[t+1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t+1] == v[t] + a_plus[t] - a_minus[t], f"Velocity_Constraint_{t}"

# Final conditions
problem += x[T] == x_T, "Final_Position"
problem += v[T] == v_T, "Final_Velocity"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')