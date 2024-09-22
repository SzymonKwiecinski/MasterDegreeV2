import pulp
import json

# Given data from the JSON format
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Define the problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define decision variables
powers = pulp.LpVariable.dicts("power", range(M), lowBound=0)

# Define the errors
errors = pulp.LpVariable.dicts("error", range(N), lowBound=0)

# Objective function: Minimize the sum of errors
problem += pulp.lpSum(errors[i] for i in range(N))

# Constraints: Calculate illumination and set error
for i in range(N):
    illumination = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    problem += illumination + errors[i] >= desired_illuminations[i]  # Illumination must be at least desired
    problem += illumination - errors[i] <= desired_illuminations[i]  # Illumination must be at most desired

# Solve the problem
problem.solve()

# Collect results
optimal_powers = [pulp.value(powers[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output results
output = {
    "power": optimal_powers,
    "error": total_error
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')