import pulp

# Data from JSON
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Extracting data
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Initialize the problem
problem = pulp.LpProblem("Lamp Power Optimization", pulp.LpMinimize)

# Decision variables for powers of lamps
power_vars = [pulp.LpVariable(f"power_{j}", lowBound=0) for j in range(M)]

# Auxiliary variables for absolute errors
error_vars = [pulp.LpVariable(f"error_{i}", lowBound=0) for i in range(N)]

# Objective function: Minimize the sum of absolute errors
problem += pulp.lpSum(error_vars)

# Constraints for each segment
for i in range(N):
    calculated_illumination = pulp.lpSum(coefficients[i][j] * power_vars[j] for j in range(M))
    # Error constraints
    problem += calculated_illumination - desired_illuminations[i] <= error_vars[i]
    problem += calculated_illumination - desired_illuminations[i] >= -error_vars[i]

# Solve the problem
problem.solve()

# Output the results in the specified format
optimal_powers = [pulp.value(power_vars[j]) for j in range(M)]
total_error = pulp.value(problem.objective)
output = {
    "power": optimal_powers,
    "error": total_error
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')