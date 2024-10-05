import pulp

# Load the data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define LP problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision variables: lamp powers
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Variables for absolute errors
abs_errors = [pulp.LpVariable(f'abs_error_{i}', lowBound=0) for i in range(N)]

# Objective function: minimize the sum of absolute errors
problem += pulp.lpSum(abs_errors)

# Constraints for absolute errors
for i in range(N):
    illumination = pulp.lpSum([coeff[i][j] * power[j] for j in range(M)])
    problem += illumination - desired[i] <= abs_errors[i], f"UpperBoundError_{i}"
    problem += desired[i] - illumination <= abs_errors[i], f"LowerBoundError_{i}"

# Solve the problem
problem.solve()

# Collect results
power_results = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output the results
output = {
    "power": power_results,
    "error": total_error
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')