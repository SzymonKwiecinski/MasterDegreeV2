import pulp
import json

# Data input
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create the LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Variables for the power of the lamps
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)

# Variables for the error (absolute difference)
error = pulp.LpVariable.dicts("error", range(N), lowBound=0)

# Objective function: Minimize the sum of errors
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Error"

# Constraints for each road segment
for i in range(N):
    problem += (pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) - desired[i] <= error[i]), f"Upper_Error_Constraint_{i}"
    problem += (desired[i] - pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) <= error[i]), f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Extracting the results
optimal_power = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output
result = {
    "power": optimal_power,
    "error": total_error
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')