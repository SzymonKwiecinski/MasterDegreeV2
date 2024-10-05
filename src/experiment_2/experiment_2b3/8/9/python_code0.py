import pulp

# Parse the input data
data = {'N': 3, 'M': 2, 'coeff': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'desired': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['coeff']
desired = data['desired']

# Initialize the problem
problem = pulp.LpProblem("Lamp_Illumination", pulp.LpMinimize)

# Define decision variables for lamp powers
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Define decision variables for absolute errors
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Define the objective function: minimize the sum of absolute errors
problem += pulp.lpSum(errors)

# Add constraints for each segment to capture the illumination and error
for i in range(N):
    illumination = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    problem += illumination - desired[i] <= errors[i]
    problem += desired[i] - illumination <= errors[i]

# Solve the problem
problem.solve()

# Retrieve the optimal powers and error
optimal_power = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output in the required format
output = {
    "power": optimal_power,
    "error": total_error
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')