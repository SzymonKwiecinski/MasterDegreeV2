import pulp

# Data from JSON
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

# Initialize the problem
problem = pulp.LpProblem("Minimize_Error", pulp.LpMinimize)

# Decision variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error_plus = [pulp.LpVariable(f'error_plus_{i}', lowBound=0) for i in range(N)]
error_minus = [pulp.LpVariable(f'error_minus_{i}', lowBound=0) for i in range(N)]

# Objective function
problem += pulp.lpSum(error_plus[i] + error_minus[i] for i in range(N))

# Constraints
for i in range(N):
    problem += (pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
                - error_plus[i] + error_minus[i] == desired_illuminations[i])

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')