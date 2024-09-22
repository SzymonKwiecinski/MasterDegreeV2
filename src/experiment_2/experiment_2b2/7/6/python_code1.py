import pulp

# Parse input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Problem
problem = pulp.LpProblem("Minimize_Fuel", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

# Auxiliary variables for absolute value handling
abs_a = [pulp.LpVariable(f"abs_a_{t}", lowBound=0, cat='Continuous') for t in range(T)]

# Objective: Minimize total fuel spent
problem += pulp.lpSum(abs_a)

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
    problem += (abs_a[t] >= a[t])  # Absolute value constraints
    problem += (abs_a[t] >= -a[t])

# Solve
problem.solve()

# Prepare output
result = {
    "x": [pulp.value(x[t]) for t in range(T+1)],
    "v": [pulp.value(v[t]) for t in range(T+1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": sum([abs(pulp.value(a[t])) for t in range(T)])
}

print(result)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")