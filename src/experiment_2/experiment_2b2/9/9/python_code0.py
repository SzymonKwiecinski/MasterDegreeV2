import pulp

# Parsing the input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the LP problem
problem = pulp.LpProblem("Illumination_Optimization", pulp.LpMinimize)

# Define decision variables for lamp powers and errors
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Set the objective function to minimize the sum of absolute errors
problem += pulp.lpSum(errors)

# Add constraints for each road segment
for i in range(N):
    problem += (pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) - desired[i] <= errors[i])
    problem += (desired[i] - pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) <= errors[i])

# Solve the LP problem
problem.solve()

# Extract results
power_values = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(pulp.lpSum(errors))

# Print objective value and results in the specified format
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
result = {
    "power": power_values,
    "error": total_error
}

print(result)