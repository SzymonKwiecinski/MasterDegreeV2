import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Variables for lamp powers
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)

# Variables for errors
error = pulp.LpVariable.dicts("error", range(N), lowBound=0)

# Objective function: Minimize sum of errors
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Error"

# Constraints for each segment
for i in range(N):
    # The illumination for segment i
    illumination = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    
    # Constraints for absolute error
    problem += illumination - desired[i] <= error[i], f"Upper_Error_Constraint_{i}"
    problem += desired[i] - illumination <= error[i], f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Extracting the results
optimal_powers = [power[j].varValue for j in range(M)]
total_error = pulp.value(problem.objective)

# Output formatting
output = {
    "power": optimal_powers,
    "error": total_error
}

# Print the results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')