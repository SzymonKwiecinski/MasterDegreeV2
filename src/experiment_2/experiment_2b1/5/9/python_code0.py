import pulp
import json

# Given data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

# Extracting coefficients and desired illuminations
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']
N = data['N']
M = data['M']

# Create the LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Decision Variables: power_j for j in 1, ..., M
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]

# Absolute errors for each segment
errors = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective function: Minimize the sum of errors
problem += pulp.lpSum(errors), "Minimize_Total_Error"

# Constraints for each segment
for i in range(N):
    # Calculate the illumination for segment i
    illumination = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    
    # Constraints for absolute error
    problem += illumination - desired_illuminations[i] <= errors[i], f"Upper_Bound_Constraint_{i}"
    problem += desired_illuminations[i] - illumination <= errors[i], f"Lower_Bound_Constraint_{i}"

# Solve the problem
problem.solve()

# Get the optimal powers and total error
optimal_powers = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Prepare the output
output = {
    "power": optimal_powers,
    "error": total_error
}

# Print results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')