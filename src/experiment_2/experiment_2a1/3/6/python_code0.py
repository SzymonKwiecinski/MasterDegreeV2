import pulp

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Problem definition
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Position", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("Velocity", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("Acceleration", range(T), lowBound=None)

# Objective function: Minimize total fuel spent
problem += pulp.lpSum(abs(a[t]) for t in range(T))

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Dynamic constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Solve the problem
problem.solve()

# Collect results
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]

# Fuel spent
fuel_spent = pulp.value(problem.objective)

# Output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')