import pulp

# Extract data from JSON
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Assign data to variables
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Initialize the problem
problem = pulp.LpProblem("RocketMotionAndFuelOptimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]

# Objective function
problem += pulp.lpSum(pulp.lpSum([pulp.lpSum([a[t] if a[t] >= 0 else -a[t]])]) for t in range(T))

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Evolution constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Solve the problem
problem.solve()

# Output results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')