import pulp

# Parse the data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define variables for lamp powers and absolute errors
power_vars = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error_vars = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective: Minimize the sum of absolute errors
problem += pulp.lpSum(error_vars)

# Constraints: Define how illumination is related to lamp powers and constrain errors
for i in range(N):
    # Compute illumination for the i-th segment
    illumination_expr = pulp.lpSum(coefficients[i][j] * power_vars[j] for j in range(M))
    desired_illumination = desired_illuminations[i]
    # Add constraints for absolute error
    problem += (illumination_expr - desired_illumination <= error_vars[i])
    problem += (desired_illumination - illumination_expr <= error_vars[i])

# Solve the problem
problem.solve()

# Get the results
optimal_power = [pulp.value(power_vars[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Format the output
output = {
    "power": optimal_power,
    "error": total_error
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')