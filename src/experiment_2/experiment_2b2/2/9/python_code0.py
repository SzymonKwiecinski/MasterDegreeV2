import pulp

# Parse the input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the problem
problem = pulp.LpProblem("LampIllumination", pulp.LpMinimize)

# Define variables
power_vars = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error_vars = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective function: Minimize total error
problem += pulp.lpSum(error_vars), "TotalError"

# Constraints
for i in range(N):
    calculated_illumination = pulp.lpSum(coefficients[i][j] * power_vars[j] for j in range(M))
    problem += (calculated_illumination - desired[i] <= error_vars[i]), f"Constraint_positive_error_segment_{i}"
    problem += (desired[i] - calculated_illumination <= error_vars[i]), f"Constraint_negative_error_segment_{i}"

# Solve the problem
problem.solve()

# Extract results
power_values = [pulp.value(power_vars[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output result format
output = {
    "power": power_values,
    "error": total_error
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')