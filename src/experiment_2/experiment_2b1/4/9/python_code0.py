import pulp
import json

# Provided data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']
N = data['N']
M = data['M']

# Create the LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Decision variables for lamp powers
powers = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Absolute errors
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: minimize the sum of errors
objective = pulp.lpSum(errors[i] for i in range(N))
problem += objective

# Constraints for each road segment
for i in range(N):
    # The illumination of segment i
    illumination = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    
    # Constraints for the error
    problem += illumination - desired_illuminations[i] <= errors[i]
    problem += desired_illuminations[i] - illumination <= errors[i]

# Solve the problem
problem.solve()

# Collect results
optimal_powers = [pulp.value(powers[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Prepare output
output = {
    "power": optimal_powers,
    "error": total_error
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')