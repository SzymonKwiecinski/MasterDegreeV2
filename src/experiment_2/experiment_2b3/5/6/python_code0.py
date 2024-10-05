import pulp

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define LP problem
problem = pulp.LpProblem("RocketTrajectory", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

# Objective: Minimize total fuel consumption
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)])

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Target conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Discrete-time model constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Solve the problem
problem.solve()

# Extract the solution
x_solution = [pulp.value(x[t]) for t in range(T + 1)]
v_solution = [pulp.value(v[t]) for t in range(T + 1)]
a_solution = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(a_solution[t]) for t in range(T))

# Output
output = {
    "x": x_solution,
    "v": v_solution,
    "a": a_solution,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')