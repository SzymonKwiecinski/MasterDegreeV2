import pulp

# Parse the input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Define the problem
problem = pulp.LpProblem("IlluminationOptimization", pulp.LpMinimize)

# Define the decision variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error = pulp.LpVariable('error', lowBound=0)

# Define the objective function
problem += error, "Minimize Absolute Error"

# Add constraints
for i in range(N):
    illum_i = sum(coeff[i][j] * power[j] for j in range(M))
    problem += illum_i - desired[i] <= error, f"Upper Bound Error for Segment {i}"
    problem += desired[i] - illum_i <= error, f"Lower Bound Error for Segment {i}"

# Solve the problem
problem.solve()

# Retrieve the results
power_values = [pulp.value(power[j]) for j in range(M)]
error_value = pulp.value(error)

# Print the results
output = {
    "power": power_values,
    "error": error_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')