import pulp

# Parse the input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create a LP problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Define decision variables for the lamp powers
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Define decision variables for the absolute errors
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective: Minimize the sum of absolute errors
problem += pulp.lpSum(errors)

# Constraints: Define the constraints for each road segment illumination
for i in range(N):
    illumination = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    problem += illumination - desired[i] <= errors[i]
    problem += desired[i] - illumination <= errors[i]

# Solve the problem
problem.solve()

# Extract the optimal values for powers and the total error
optimal_powers = [pulp.value(power_var) for power_var in power]
total_error = pulp.value(problem.objective)

# Prepare the output
output = {
    "power": optimal_powers,
    "error": total_error
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')