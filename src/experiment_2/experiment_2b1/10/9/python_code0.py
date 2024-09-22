import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Create decision variables for lamp powers
powers = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Create variables to capture error
error = pulp.LpVariable("Error", lowBound=0)

# Objective function: minimize the sum of errors
problem += error

# Constraints to formulate the absolute error
for i in range(N):
    # Calculate illumination for segment i
    illumination = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    
    # Constraints for the absolute error
    problem += illumination - desired_illuminations[i] <= error
    problem += desired_illuminations[i] - illumination <= error

# Solve the problem
problem.solve()

# Preparing the output
output = {
    "power": [pulp.value(powers[j]) for j in range(M)],
    "error": pulp.value(error)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# JSON output
print(json.dumps(output))