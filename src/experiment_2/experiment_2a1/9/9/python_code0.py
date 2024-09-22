import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define decision variables
powers = pulp.LpVariable.dicts("power", range(M), lowBound=0)  # powers of the lamps

# Define the absolute errors
errors = pulp.LpVariable.dicts("error", range(N), lowBound=0)

# Objective function: minimize the sum of errors
problem += pulp.lpSum(errors[i] for i in range(N)), "Total_Absolute_Error"

# Constraints: Define the illumination for each segment and the relationship with the errors
for i in range(N):
    # Calculate the illumination for segment i
    illumination = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    
    # Constraints for absolute errors
    problem += illumination + errors[i] >= desired[i], f"UpperBoundError_{i}"
    problem += illumination - errors[i] <= desired[i], f"LowerBoundError_{i}"

# Solve the problem
problem.solve()

# Prepare the output
optimal_powers = [pulp.value(powers[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output result
output = {
    "power": optimal_powers,
    "error": total_error
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')