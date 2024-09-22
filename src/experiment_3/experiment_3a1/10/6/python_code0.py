import pulp

# Data from the provided JSON
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create the optimization problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]

# Objective function: minimize total fuel consumption
problem += pulp.lpSum([pulp.abs(a[t]) for t in range(T)])

# Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

# Constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])  # Position update
    problem += (v[t + 1] == v[t] + a[t])  # Velocity update

# Final conditions
problem += (x[T] == x[T - 1] + v[T - 1])  # Final position
problem += (v[T] == v[T - 1] + a[T - 1])  # Final velocity

# Solve the problem
problem.solve()

# Output results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
total_fuel_spent = pulp.value(problem.objective)

# Print objective
print(f' (Objective Value): <OBJ>{total_fuel_spent}</OBJ>')

# Print the results
print("x:", x_values)
print("v:", v_values)
print("a:", a_values)
print("total_fuel_spent:", total_fuel_spent)