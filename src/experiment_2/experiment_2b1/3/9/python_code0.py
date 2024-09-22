import json
import pulp

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired = data['DesiredIlluminations']

# Create LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Variables: power_j for j-th lamp
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Objective: Minimize the absolute error
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Add objective function
problem += pulp.lpSum(errors), "Minimize_Absolute_Error"

# Constraints to capture the absolute error
for i in range(N):
    problem += pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) - errors[i] <= desired[i], f"Upper_Error_Constraint_{i}"
    problem += errors[i] <= pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) - desired[i], f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare the output
optimal_power = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output the results
output = {
    "power": optimal_power,
    "error": total_error
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')