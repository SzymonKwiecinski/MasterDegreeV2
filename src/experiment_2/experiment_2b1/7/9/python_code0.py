import pulp
import json

# Provided data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

# Extracting coefficients and desired illuminations
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Create decision variables for lamp powers
powers = pulp.LpVariable.dicts("Power", range(M), lowBound=0)  # assuming non-negative powers

# Create variables for absolute errors
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: minimize the sum of absolute errors
problem += pulp.lpSum(errors[i] for i in range(N)), "Total_Error"

# Adding constraints for each segment
for i in range(N):
    # The illumination calculated for the i-th segment
    illumination = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    # Constraints for absolute errors
    problem += illumination + errors[i] >= desired_illuminations[i], f"Upper_Error_Constraint_{i}"
    problem += illumination - errors[i] <= desired_illuminations[i], f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Collect results
optimal_powers = [pulp.value(powers[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output format
result = {
    "power": optimal_powers,
    "error": total_error
}

# Print the output
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')