import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

# Extracting the problem parameters from data
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create the LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define decision variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error = pulp.LpVariable('error', lowBound=0)

# Objective function: minimize the total error 
problem += error, "Minimize_Total_Error"

# Adding constraints for each segment
for i in range(N):
    # Create a constraint for the absolute error
    problem += (pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) - desired[i] <= error, f"Upper_Bound_Constraint_{i}")
    problem += (desired[i] - pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) <= error, f"Lower_Bound_Constraint_{i}")

# Solve the problem
problem.solve()

# Extract the results
optimal_power = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(error)

# Output format
output = {
    "power": optimal_power,
    "error": total_error
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# The output
print(json.dumps(output))