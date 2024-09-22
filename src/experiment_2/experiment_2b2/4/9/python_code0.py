import pulp

# Extracting data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("LampPowerOptimization", pulp.LpMinimize)

# Variables
power_vars = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error_vars = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective: Minimize sum of absolute errors
problem += pulp.lpSum(error_vars)

# Constraints for absolute error
for i in range(N):
    illumination = pulp.lpSum(coefficients[i][j] * power_vars[j] for j in range(M))
    problem += illumination - desired_illuminations[i] <= error_vars[i]
    problem += desired_illuminations[i] - illumination <= error_vars[i]

# Solve
problem.solve()

# Collecting results
power_values = [pulp.value(var) for var in power_vars]
total_error = sum(pulp.value(var) for var in error_vars)

# Output
result = {
    "power": power_values,
    "error": total_error
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')