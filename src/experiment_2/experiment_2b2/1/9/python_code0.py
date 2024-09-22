import pulp

# Read data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("IlluminationOptimization", pulp.LpMinimize)

# Decision variables: power of each lamp
power_vars = [pulp.LpVariable(f"power_{j}", lowBound=0, cat='Continuous') for j in range(M)]

# Error variables for each road segment absolute error |ill_i - desired_i|
error_vars = [pulp.LpVariable(f"error_{i}", lowBound=0, cat='Continuous') for i in range(N)]

# Objective: minimize the sum of absolute errors
problem += pulp.lpSum(error_vars)

# Constraints: Calculate the absolute error for each segment
for i in range(N):
    illumination = pulp.lpSum(coeff[i][j] * power_vars[j] for j in range(M))
    # Constraints for absolute values
    problem += (illumination - desired[i] <= error_vars[i]), f"Positive_Error_Constraint_{i}"
    problem += (desired[i] - illumination <= error_vars[i]), f"Negative_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Extract the results
power_results = [pulp.value(power_vars[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output format
result = {
    "power": power_results,
    "error": total_error
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')