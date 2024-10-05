import pulp

# Extract data from the provided JSON format
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Initialize the problem
problem = pulp.LpProblem("LampPowerOptimization", pulp.LpMinimize)

# Decision variables
power = [pulp.LpVariable(f"Power_{j}", lowBound=0) for j in range(M)]
error_vars = [pulp.LpVariable(f"Error_{i}", lowBound=0) for i in range(N)]

# Objective: Minimize the sum of absolute errors
problem += pulp.lpSum(error_vars)

# Constraints
for i in range(N):
    # Illumination constraint: illum_i = sum(coeff[i][j] * power[j]) and error handling
    illum_i = pulp.lpSum([coeff[i][j] * power[j] for j in range(M)])
    problem += illum_i - desired[i] <= error_vars[i]
    problem += desired[i] - illum_i <= error_vars[i]

# Solve the problem
problem.solve()

# Output
result_power = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Print the results in the required format
output = {
    "power": result_power,
    "error": total_error
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')