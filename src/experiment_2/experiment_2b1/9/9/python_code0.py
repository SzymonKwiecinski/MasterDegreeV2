import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

# Problem setup
N = data['N']  # number of segments
M = data['M']  # number of lamps
coefficients = data['Coefficients']  # coefficients for illumination
desired_illuminations = data['DesiredIlluminations']  # desired illumination levels

# Create the problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Define decision variables for lamp powers
powers = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Define the absolute error variables
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: minimize the sum of errors
problem += pulp.lpSum(errors[i] for i in range(N)), "Total_Error"

# Constraints to link power and desired illumination
for i in range(N):
    problem += (pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M)) - desired_illuminations[i] == errors[i]), f"Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare output
optimal_powers = [pulp.value(powers[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

output_data = {
    "power": optimal_powers,
    "error": total_error
}

# Print result
print(json.dumps(output_data))
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')