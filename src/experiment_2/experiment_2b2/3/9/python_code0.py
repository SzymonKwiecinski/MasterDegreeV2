import pulp

# Data from input
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Unpack the data
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create the LP problem
problem = pulp.LpProblem("Lamp_Illumination_Problem", pulp.LpMinimize)

# Define variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0, cat='Continuous') for j in range(M)]
errors = [pulp.LpVariable(f'error_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Define objective function
problem += pulp.lpSum(errors)

# Add constraints to relate errors and desired illuminations
for i in range(N):
    ill_i = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    problem += ill_i - desired[i] <= errors[i]
    problem += desired[i] - ill_i <= errors[i]

# Solve the problem
problem.solve()

# Extract results
power_values = [pulp.value(power_j) for power_j in power]
total_error = pulp.value(problem.objective)

# Print results
result = {
    "power": power_values,
    "error": total_error
}
print(result)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')