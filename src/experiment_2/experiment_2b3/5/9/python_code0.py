import pulp

# Define the data
data = {
    'N': 3,
    'M': 2,
    'coeff': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'desired': [14, 3, 12]
}

# Extract data
N = data['N']
M = data['M']
coeff = data['coeff']
desired = data['desired']

# Define the problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision variables for lamp powers
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
# Auxiliary variables for absolute errors
abs_errors = [pulp.LpVariable(f'abs_error_{i}', lowBound=0) for i in range(N)]

# Objective function: minimize the total absolute error
problem += pulp.lpSum(abs_errors)

# Constraints: calculate the errors
for i in range(N):
    illumination = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    problem += illumination - desired[i] <= abs_errors[i]
    problem += desired[i] - illumination <= abs_errors[i]

# Solve the problem
problem.solve()

# Extract results
result_powers = [pulp.value(power[j]) for j in range(M)]
error = pulp.value(problem.objective)

# Prepare the output
output = {
    "power": result_powers,
    "error": error
}

# Print the output
print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')