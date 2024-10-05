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
problem = pulp.LpProblem("Optimal_Lamp_Powers", pulp.LpMinimize)

# Variables
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]
powers = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Objective
problem += pulp.lpSum(errors)

# Constraints
for i in range(N):
    lhs = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    problem += errors[i] >= lhs - desired_illuminations[i]
    problem += errors[i] >= -(lhs - desired_illuminations[i])

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')