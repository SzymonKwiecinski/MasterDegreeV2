import pulp

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create a linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Define decision variables
a = [pulp.LpVariable(f'a_{t}') for t in range(T-1)]  # acceleration
x = [pulp.LpVariable(f'x_{t}') for t in range(T)]     # position
v = [pulp.LpVariable(f'v_{t}') for t in range(T)]     # velocity

# Objective function: Minimize total fuel spent
problem += pulp.lpSum([pulp.abs(a[t]) for t in range(T-1)])

# Constraints
problem += x[0] == x_0  # Initial position
problem += v[0] == v_0  # Initial velocity

for t in range(T-1):
    problem += x[t+1] == x[t] + v[t]  # Position update
    problem += v[t+1] == v[t] + a[t]  # Velocity update

problem += x[T-1] == x_T  # Final position constraint
problem += v[T-1] == v_T  # Final velocity constraint

# Solve the problem
problem.solve()

# Get the results
positions = [x[t].varValue for t in range(T)]
velocities = [v[t].varValue for t in range(T)]
accelerations = [a[t].varValue for t in range(T-1)]
total_fuel_spent = pulp.value(problem.objective)

# Outputs
print(f"Positions: {positions}")
print(f"Velocities: {velocities}")
print(f"Accelerations: {accelerations}")
print(f' (Objective Value): <OBJ>{total_fuel_spent}</OBJ>')