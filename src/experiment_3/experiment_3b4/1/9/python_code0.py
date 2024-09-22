import pulp

# Data provided
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Number of road segments and lamps
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the LP minimization problem
problem = pulp.LpProblem("Minimize_Total_Absolute_Error", pulp.LpMinimize)

# Decision variables for power
power_vars = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(1, M + 1)]

# Auxiliary variables for positive and negative errors
error_plus_vars = [pulp.LpVariable(f'error_plus_{i}', lowBound=0) for i in range(1, N + 1)]
error_minus_vars = [pulp.LpVariable(f'error_minus_{i}', lowBound=0) for i in range(1, N + 1)]

# Objective function: Minimize the total absolute error
problem += pulp.lpSum(error_plus_vars[i] + error_minus_vars[i] for i in range(N))

# Constraints
for i in range(N):
    problem += (pulp.lpSum(coefficients[i][j] * power_vars[j] for j in range(M)) ==
                desired_illuminations[i] + error_plus_vars[i] - error_minus_vars[i])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')