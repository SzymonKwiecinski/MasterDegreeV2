import pulp

# Data from JSON
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

# Define the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Create variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')

# Objective: Minimize total fuel spent
problem += pulp.lpSum(a[t] for t in range(T))

# Constraints
# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Position and velocity constraints over time
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Solve the problem
problem.solve()

# Collect results
x_values = [pulp.value(x[i]) for i in range(1, T+1)]
v_values = [pulp.value(v[i]) for i in range(1, T+1)]
a_values = [pulp.value(a[i]) for i in range(T)]

# Output the results
print("Position x:", x_values)
print("Velocity v:", v_values)
print("Acceleration a:", a_values)
print(f'Fuel spend: {pulp.value(problem.objective)}')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')