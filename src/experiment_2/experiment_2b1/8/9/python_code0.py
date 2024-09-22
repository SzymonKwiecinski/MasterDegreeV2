import pulp
import json

# Data extraction from JSON
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Problem definition
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision variables for lamp powers
powers = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Error variables for absolute differences
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: minimize the sum of errors
problem += pulp.lpSum(errors[i] for i in range(N))

# Constraints to define the errors
for i in range(N):
    illumination = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    problem += illumination + errors[i] >= desired_illuminations[i]
    problem += illumination - errors[i] <= desired_illuminations[i]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "power": [pulp.value(powers[j]) for j in range(M)],
    "error": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output as JSON format
print(json.dumps(output))