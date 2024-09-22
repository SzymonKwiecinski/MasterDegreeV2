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
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("Road_Illumination_Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
abs_errors = [pulp.LpVariable(f'abs_error_{i}', lowBound=0) for i in range(N)]

# Illumination and Objective
for i in range(N):
    illum = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    problem += abs_errors[i] >= illum - desired[i]
    problem += abs_errors[i] >= desired[i] - illum

problem += pulp.lpSum(abs_errors)

# Solve
problem.solve()

# Print Results
optimal_powers = [pulp.value(power[j]) for j in range(M)]
absolute_error = pulp.value(problem.objective)

print(f'Optimal Power for Each Lamp: {optimal_powers}')
print(f'(Objective Value): <OBJ>{absolute_error}</OBJ>')