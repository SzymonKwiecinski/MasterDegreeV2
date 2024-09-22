import pulp

# Parse the input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the LP problem
problem = pulp.LpProblem("LampPowerOptimization", pulp.LpMinimize)

# Define the variables for lamp powers
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Absolute error variables
abs_error = [pulp.LpVariable(f'abs_error_{i}', lowBound=0) for i in range(N)]

# Define the objective function: minimize the sum of absolute errors
problem += pulp.lpSum(abs_error)

# Add constraints for each segment
for i in range(N):
    # Calculate the illumination of each segment
    illumination = pulp.lpSum([coeff[i][j] * power[j] for j in range(M)])
    # Add constraints to model the absolute error
    problem += illumination - desired[i] <= abs_error[i]
    problem += desired[i] - illumination <= abs_error[i]

# Solve the problem
problem.solve()

# Retrieve the results
optimal_power = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output results
output = {
    "power": optimal_power,
    "error": total_error
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')