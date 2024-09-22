import pulp

# Read the data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the LP problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Define the decision variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
abs_errors = [pulp.LpVariable(f'abs_error_{i}', lowBound=0) for i in range(N)]

# Objective function: Minimize the sum of absolute errors
problem += pulp.lpSum(abs_errors)

# Constraints: Calculate the absolute error for each segment
for i in range(N):
    problem += pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) - desired[i] <= abs_errors[i]
    problem += desired[i] - pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) <= abs_errors[i]

# Solve the problem
problem.solve()

# Extract the solution
power_values = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(pulp.lpSum(abs_errors))

# Prepare the output in the specified format
output = {
    "power": power_values,
    "error": total_error
}

# Print the output and the objective
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')