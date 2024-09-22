import pulp

# Read data from input
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Reading parameters from the given data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define the problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]

# Objective function: Minimize total absolute acceleration (fuel)
problem += pulp.lpSum([pulp.lpAbs(a_t) for a_t in a])

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Constraints for each time step
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

# Solve the problem
problem.solve()

# Gather results
x_vals = [pulp.value(x_t) for x_t in x]
v_vals = [pulp.value(v_t) for v_t in v]
a_vals = [pulp.value(a_t) for a_t in a]
fuel_spent = sum(abs(a_t) for a_t in a_vals)

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Prepare the output in the required format
output = {
    "x": x_vals,
    "v": v_vals,
    "a": a_vals,
    "fuel_spend": fuel_spent,
}

print(output)