import pulp

# Data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("LampPowerOptimization", pulp.LpMinimize)

# Variables
power_vars = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error_vars = [pulp.LpVariable(f'error_{i}') for i in range(N)]

# Objective Function
problem += pulp.lpSum(error_vars)

# Constraints
for i in range(N):
    ill_i = pulp.lpSum(coefficients[i][j] * power_vars[j] for j in range(M))
    problem += (ill_i - desired_illuminations[i] <= error_vars[i])
    problem += (-ill_i + desired_illuminations[i] <= error_vars[i])

# Solve
problem.solve()

# Results
optimal_powers = [pulp.value(power_vars[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output
output = {
    "power": optimal_powers,
    "error": total_error
}

print("Optimal Lamp Powers:", output['power'])
print("Total Error:", output['error'])
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')