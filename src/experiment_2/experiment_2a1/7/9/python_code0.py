import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create a problem variable 
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Define variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Define the error variables
error = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: Minimize the total error
problem += pulp.lpSum(error[i] for i in range(N))

# Constraints for each segment
for i in range(N):
    problem += (pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) - desired[i] <= error[i])
    problem += (desired[i] - pulp.lpSum(coeff[i][j] * power[j] for j in range(M)) <= error[i])

# Solve the problem
problem.solve()

# Extract results
optimal_power = [power[j].varValue for j in range(M)]
total_error = pulp.value(problem.objective)

# Output the results in the required format
result = {
    "power": optimal_power,
    "error": total_error
}

print(result)
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')