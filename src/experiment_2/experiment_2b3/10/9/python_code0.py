import pulp

# Load the data
data = {
    'N': 3, 
    'M': 2, 
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 
    'DesiredIlluminations': [14, 3, 12]
}

# Extract data
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Initialize the problem
problem = pulp.LpProblem("IlluminationOptimization", pulp.LpMinimize)

# Decision variables for lamp power
powers = [pulp.LpVariable(f'power_{j+1}', lowBound=0) for j in range(M)]

# Error terms
errors = [pulp.LpVariable(f'error_{i+1}', lowBound=0) for i in range(N)]

# Define the objective function to minimize the sum of errors
problem += pulp.lpSum(errors)

# Constraints for the illumination at each segment
for i in range(N):
    # Calculate illumination at segment i
    illumination = pulp.lpSum(coeff[i][j] * powers[j] for j in range(M))
    problem += (illumination - desired[i] <= errors[i])
    problem += (desired[i] - illumination <= errors[i])

# Solve the problem
problem.solve()

# Extract results
output = {
    "power": [pulp.value(powers[j]) for j in range(M)],
    "error": sum(pulp.value(errors[i]) for i in range(N))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')