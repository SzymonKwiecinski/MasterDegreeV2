import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Define variables for lamp powers
powers = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Define the absolute errors for each segment
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: minimize the sum of errors
problem += pulp.lpSum(errors[i] for i in range(N)), "Total_Error"

# Constraints for each segment illumination
for i in range(N):
    illumination = pulp.lpSum(coeff[i][j] * powers[j] for j in range(M))
    problem += illumination - desired[i] <= errors[i], f"Upper_Error_Segment_{i}"
    problem += desired[i] - illumination <= errors[i], f"Lower_Error_Segment_{i}"

# Solve the problem
problem.solve()

# Get the results
optimal_powers = [powers[j].varValue for j in range(M)]
total_error = pulp.value(problem.objective)

# Format output
output = {
    "power": optimal_powers,
    "error": total_error
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')