import pulp

# Data from the input
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the problem
problem = pulp.LpProblem("RocketControl", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T+1), cat="Continuous")
v = pulp.LpVariable.dicts("v", range(T+1), cat="Continuous")
a = pulp.LpVariable.dicts("a", range(T), lowBound=-1, upBound=1, cat="Continuous")

# Additional variables for absolute value of acceleration
a_abs = pulp.LpVariable.dicts("a_abs", range(T), lowBound=0, cat="Continuous")

# Objective: Minimize total fuel consumption
problem += pulp.lpSum([a_abs[t] for t in range(T)])

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])

# Absolute value constraints
for t in range(T):
    problem += (a_abs[t] >= a[t])
    problem += (a_abs[t] >= -a[t])

# Solve the problem
problem.solve()

# Retrieve results
x_values = [pulp.value(x[i]) for i in range(T+1)]
v_values = [pulp.value(v[i]) for i in range(T+1)]
a_values = [pulp.value(a[i]) for i in range(T)]
fuel_spent = sum(pulp.value(a_abs[t]) for t in range(T))

# Print the results
result = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}
print(result)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')