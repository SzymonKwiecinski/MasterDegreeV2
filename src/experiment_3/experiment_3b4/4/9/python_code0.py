import pulp

# Data input
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

# Define the problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision variables
power_vars = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error_vars = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective function
problem += pulp.lpSum(error_vars)

# Constraints
for i in range(N):
    ill_i = pulp.lpSum(coefficients[i][j] * power_vars[j] for j in range(M))
    problem += error_vars[i] >= ill_i - desired_illuminations[i]
    problem += error_vars[i] >= desired_illuminations[i] - ill_i

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')