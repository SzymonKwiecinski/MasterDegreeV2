import pulp

# Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Extracting the data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the problem
problem = pulp.LpProblem('RocketMotionOptimization', pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), cat=pulp.LpContinuous)
v = pulp.LpVariable.dicts("v", range(T + 1), cat=pulp.LpContinuous)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, cat=pulp.LpContinuous)

# Objective function: Minimize the total fuel consumption
problem += pulp.lpSum(pulp.lpSum([pulp.lpSum([abs(a[t])]) for t in range(T)]))

# Constraints
# Initial conditions
problem += x[0] == x_0, "Initial Position"
problem += v[0] == v_0, "Initial Velocity"

# Final conditions
problem += x[T] == x_T, "Final Position"
problem += v[T] == v_T, "Final Velocity"

# Motion constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position update at {t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity update at {t}"

# Solve the problem
problem.solve()

# Output the results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]

result = {
    'x': x_values,
    'v': v_values,
    'a': a_values,
    'fuel_spend': pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')