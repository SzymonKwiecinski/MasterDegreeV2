import pulp

# Data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("IlluminationProblem", pulp.LpMinimize)

# Variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective
problem += pulp.lpSum(error)

# Constraints
for i in range(N):
    illumination = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    problem += illumination - desired_illuminations[i] <= error[i]
    problem += desired_illuminations[i] - illumination <= error[i]

# Solve
problem.solve()

# Print results
for j in range(M):
    print(f'Power of lamp {j + 1}: {pulp.value(power[j])}')

print(f'Total illumination error: {pulp.value(problem.objective)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')