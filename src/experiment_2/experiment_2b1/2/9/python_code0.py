import pulp
import json

# Input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired = data['DesiredIlluminations']

# Create the problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Define the absolute errors
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: minimize the sum of errors
problem += pulp.lpSum(errors[i] for i in range(N)), "Minimize_Absolute_Error"

# Constraints based on the illumination equations
for i in range(N):
    # Calculate the illumination for segment i
    illumination = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    
    # Constraints for the absolute error
    problem += illumination - desired[i] <= errors[i], f"Upper_Error_Constraint_{i}"
    problem += desired[i] - illumination <= errors[i], f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Gather results
optimal_power = [power[j].varValue for j in range(M)]
total_error = sum(errors[i].varValue for i in range(N))

# Output results
output = {
    "power": optimal_power,
    "error": total_error
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')