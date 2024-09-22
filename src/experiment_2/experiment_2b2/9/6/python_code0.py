import pulp

# Parse the input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the linear programming problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

# Decision variables for positions, velocities and accelerations
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

# Add absolute value variables for accelerations
abs_a = [pulp.LpVariable(f"abs_a_{t}", lowBound=0, cat='Continuous') for t in range(T)]

# Objective is to minimize the total fuel spent, which is the sum of absolute accelerations
problem += pulp.lpSum(abs_a)

# Initial conditions
problem += (x[0] == x_0, "InitialPosition")
problem += (v[0] == v_0, "InitialVelocity")

# Final conditions
problem += (x[T] == x_T, "FinalPosition")
problem += (v[T] == v_T, "FinalVelocity")

# Dynamic equations for the trajectory
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionEquation_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityEquation_{t}")
    
    # Constraints for absolute value of acceleration
    problem += (abs_a[t] >= a[t], f"AbsConstraintPos_{t}")
    problem += (abs_a[t] >= -a[t], f"AbsConstraintNeg_{t}")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "x": [pulp.value(x[t]) for t in range(T + 1)],
    "v": [pulp.value(v[t]) for t in range(T + 1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

# Print the output
print(output)

# Print the objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")