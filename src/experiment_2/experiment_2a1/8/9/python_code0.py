import pulp
import json

# Data input
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired = data['DesiredIlluminations']

# Initialize the LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Decision variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Create variables for error terms
error_terms = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective function: minimize the sum of error terms
problem += pulp.lpSum(error_terms)

# Constraints to calculate the errors
for i in range(N):
    # Illumination equation
    illumination = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    # Constraint for absolute error
    problem += illumination >= desired[i] - error_terms[i]
    problem += illumination <= desired[i] + error_terms[i]

# Solve the problem
problem.solve()

# Extract results
optimal_power = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Prepare output
output = {
    "power": optimal_power,
    "error": total_error
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')