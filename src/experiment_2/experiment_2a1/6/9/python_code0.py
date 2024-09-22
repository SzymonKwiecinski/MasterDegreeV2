import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

# Extract the number of segments and lamps
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Initialize the LP problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Define lamp power variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)

# Define the absolute error variables
errors = pulp.LpVariable.dicts("error", range(N), lowBound=0)

# Objective function: Minimize the sum of all errors
problem += pulp.lpSum(errors[i] for i in range(N))

# Constraints to ensure errors are calculated correctly
for i in range(N):
    # Calculate the illumination for segment i
    illumination_expr = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    
    # The absolute error constraints
    problem += illumination_expr - desired_illuminations[i] <= errors[i]
    problem += desired_illuminations[i] - illumination_expr <= errors[i]

# Solve the problem
problem.solve()

# Gather results
result_power = [power[j].varValue for j in range(M)]
result_error = pulp.value(problem.objective)

# Prepare output
output = {
    "power": result_power,
    "error": result_error
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')