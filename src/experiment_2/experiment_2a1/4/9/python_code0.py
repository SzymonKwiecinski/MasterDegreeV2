import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Variables for power of each lamp
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Variables for absolute errors
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective function: minimize the sum of errors
problem += pulp.lpSum(errors)

# Constraints: ill_i = sum(coeff_{i,j} * power_j) + error_i
for i in range(N):
    illumination = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    problem += illumination + errors[i] >= desired[i]
    problem += illumination - errors[i] <= desired[i]

# Solve the problem
problem.solve()

# Extract results
optimal_powers = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Create output
output = {
    "power": optimal_powers,
    "error": total_error
}

# Print results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')