import pulp

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 
        'FinalVelocity': 0, 'TotalTime': 20}

# Parameters
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the optimization problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable.dicts("a", range(T-1), lowBound=None)  # Acceleration

# State Variables (for each time step)
x = pulp.LpVariable.dicts("x", range(T), lowBound=None)   # Position
v = pulp.LpVariable.dicts("v", range(T), lowBound=None)   # Velocity

# Objective Function: Minimize total fuel consumption
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T-1)])

# Initial conditions
problem += (x[0] == x_0, "InitialPosition")
problem += (v[0] == v_0, "InitialVelocity")

# Final conditions
problem += (x[T-1] == x_T, "FinalPosition")
problem += (v[T-1] == v_T, "FinalVelocity")

# Constraints for dynamics
for t in range(T-1):
    problem += (x[t+1] == x[t] + v[t], f"PositionUpdate_{t}")
    problem += (v[t+1] == v[t] + a[t], f"VelocityUpdate_{t}")

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')