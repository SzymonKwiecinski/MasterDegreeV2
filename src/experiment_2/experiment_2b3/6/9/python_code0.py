import pulp

# Data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Variables
powers = [pulp.LpVariable(f'power_{j+1}', lowBound=0) for j in range(M)]
errors = [pulp.LpVariable(f'error_{i+1}', lowBound=0) for i in range(N)]

# Objective
problem += pulp.lpSum(errors)

# Constraints
for i in range(N):
    illumination = pulp.lpSum(coeff[i][j] * powers[j] for j in range(M))
    problem += illumination - desired[i] <= errors[i]
    problem += desired[i] - illumination <= errors[i]

# Solve
problem.solve()

# Results
powers_result = [pulp.value(powers[j]) for j in range(M)]
error_result = pulp.value(problem.objective)

result = {
    "power": powers_result,
    "error": error_result
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')