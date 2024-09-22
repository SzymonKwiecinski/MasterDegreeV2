import pulp

# Define the problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Extract data from JSON
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
coeff = data['Coefficients']
desired = data['DesiredIlluminations']
N = data['N']
M = data['M']

# Define decision variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Define auxiliary variables for absolute error
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective function: Minimize the sum of absolute errors
problem += pulp.lpSum(errors)

# Constraints for each segment's illumination and absolute error
for i in range(N):
    illumination = pulp.lpSum([coeff[i][j] * power[j] for j in range(M)])
    problem += illumination - desired[i] <= errors[i]
    problem += desired[i] - illumination <= errors[i]

# Solve the problem
problem.solve()

# Extract the results
power_solution = [pulp.value(power[j]) for j in range(M)]
error = pulp.value(problem.objective)

# Print the results
print({
    "power": power_solution,
    "error": error
})
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')