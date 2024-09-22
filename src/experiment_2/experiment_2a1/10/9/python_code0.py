import pulp
import json

# Given data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create a problem variable
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define decision variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Define the errors
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: minimize the sum of errors
problem += pulp.lpSum(errors[i] for i in range(N))

# Constraints for illuminations
for i in range(N):
    problem += (pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) - desired_illuminations[i] <= errors[i])
    problem += (desired_illuminations[i] - pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) <= errors[i])

# Solve the problem
problem.solve()

# Gather results
optimized_power = [power[j].varValue for j in range(M)]
total_error = pulp.value(problem.objective)

# Output the results in the specified format
output = {
    "power": optimized_power,
    "error": total_error
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')