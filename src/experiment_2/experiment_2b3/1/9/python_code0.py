import pulp

# Loading data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define LP Problem
problem = pulp.LpProblem("LampPowerOptimization", pulp.LpMinimize)

# Variables: power_j for each lamp
power_vars = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Variables: absolute errors for each road segment
error_vars = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective: Minimize the sum of absolute errors
problem += pulp.lpSum(error_vars)

# Constraints: Calculate illumination and error for each segment
for i in range(N):
    illumination = pulp.lpSum(coeff[i][j] * power_vars[j] for j in range(M))
    problem += (illumination - desired[i] <= error_vars[i])
    problem += (desired[i] - illumination <= error_vars[i])

# Solve the problem
problem.solve()

# Extracting results
powers = [pulp.value(power_vars[j]) for j in range(M)]
total_error = pulp.value(pulp.lpSum(error_vars))

result = {
    "power": powers,
    "error": total_error
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')