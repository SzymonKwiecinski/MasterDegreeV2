import json
import pulp

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective function: minimize the total error
problem += pulp.lpSum(errors)

# Constraints for each segment of the road
for i in range(N):
    ill_i = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    problem += ill_i >= desired[i] - errors[i]
    problem += ill_i <= desired[i] + errors[i]

# Solve the problem
problem.solve()

# Retrieve the results
optimal_power = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output the results
result = {
    "power": optimal_power,
    "error": total_error
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')