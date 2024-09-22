import pulp

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Initialize the LP problem
problem = pulp.LpProblem("Rocket_Problem", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity

# Objective function: Minimize total fuel spent (sum of absolute accelerations)
problem += pulp.lpSum([a[t] for t in range(T)])

# Constraints
# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Dynamics constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]

# Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

# Solve the problem
problem.solve()

# Extract the results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Output the results
result = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(result)
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')