from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpStatus, value
import json

# Load the data
data = json.loads('{"N": 3, "M": 2, "Coefficients": [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], "DesiredIlluminations": [14, 3, 12]}')

N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Initialize the optimization problem
problem = LpProblem("Optimal_Lamp_Powers", LpMinimize)

# Define variables
power = [LpVariable(f'power_{j}', lowBound=0) for j in range(1, M+1)]
error = LpVariable('error', lowBound=0)

# Add absolute error constraints
for i in range(N):
    illumination_i = lpSum([coeff[i][j] * power[j] for j in range(M)])
    problem += (illumination_i <= desired[i] + error, f'Illumination{1}_UpperBound')
    problem += (illumination_i >= desired[i] - error, f'Illumination{1}_LowerBound')

# Define the objective function
problem += error, "Objective"

# Solve the problem
problem.solve()

# Collect results
results = {
    "power": [value(power[j]) for j in range(M)],
    "error": value(error)
}

# Output the results
output_json = json.dumps(results, indent=4)
print(output_json)

# Print the objective value
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')