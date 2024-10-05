import pulp

# Extracting data from the provided JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the LP problem
problem = pulp.LpProblem("Rocket_Optimization", pulp.LpMinimize)

# Decision variables for position, velocity, and acceleration
x = pulp.LpVariable.dicts("Position", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("Velocity", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("Acceleration", range(T), lowBound=None, cat='Continuous')

# Absolute value variables for acceleration
abs_a = pulp.LpVariable.dicts("Abs_Acceleration", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize total absolute acceleration (fuel consumption)
problem += pulp.lpSum(abs_a[t] for t in range(T))

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Equations of motion and constraints
for t in range(T):
    # Position constraint
    problem += (x[t+1] == x[t] + v[t])
    # Velocity constraint
    problem += (v[t+1] == v[t] + a[t])
    # Absolute value constraints for acceleration
    problem += (abs_a[t] >= a[t])
    problem += (abs_a[t] >= -a[t])

# Final desired position and velocity
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Solve the LP problem
problem.solve()

# Extract the results
output = {
    "x": [pulp.value(x[t]) for t in range(T+1)],
    "v": [pulp.value(v[t]) for t in range(T+1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": sum(pulp.value(abs_a[t]) for t in range(T))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')