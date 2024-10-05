import pulp

# Data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create the problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision variables
power_vars = [pulp.LpVariable(f'power_{j+1}', lowBound=0, cat='Continuous') for j in range(M)]
error_vars = [pulp.LpVariable(f'error_{i+1}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective function
problem += pulp.lpSum(error_vars)

# Constraints
for i in range(N):
    illum = pulp.lpSum(coeff[i][j] * power_vars[j] for j in range(M))
    problem += illum - desired[i] <= error_vars[i]
    problem += desired[i] - illum <= error_vars[i]

# Solve the problem
problem.solve()

# Output
output = {
    "power": [pulp.value(power_vars[j]) for j in range(M)],
    "error": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')