import pulp
import json

# Data from JSON format
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the Linear Programming problem
problem = pulp.LpProblem("Illumination_Minimization", pulp.LpMinimize)

# Decision variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Calculate the actual illumination for each road segment
illuminations = [pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) for i in range(N)]

# Objective function: Minimize the absolute error
absolute_errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]
for i in range(N):
    problem += illuminations[i] - desired_illuminations[i] <= absolute_errors[i]
    problem += desired_illuminations[i] - illuminations[i] <= absolute_errors[i]

# Objective: Minimize the total absolute error
problem += pulp.lpSum(absolute_errors)

# Solve the problem
problem.solve()

# Extract the results
power_values = [pulp.value(power[j]) for j in range(M)]
error = pulp.value(problem.objective)

# Print the results
print(f'Optimal power values for each lamp: {power_values}')
print(f' (Objective Value): <OBJ>{error}</OBJ>')