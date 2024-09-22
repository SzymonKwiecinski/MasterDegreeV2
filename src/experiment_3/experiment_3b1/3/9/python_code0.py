import pulp
import json

# Data initialization
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the problem
problem = pulp.LpProblem("Road_Illumination_Optimization", pulp.LpMinimize)

# Decision variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)  # power_j >= 0
error = pulp.LpVariable.dicts("Error", range(N), lowBound=0)   # e_i >= 0

# Objective function
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Absolute_Error"

# Constraints for each segment
for i in range(N):
    # Calculate ill_i
    ill_i = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    # Constraints for absolute error
    problem += ill_i - desired_illuminations[i] <= error[i], f"Error_Positive_{i}"
    problem += desired_illuminations[i] - ill_i <= error[i], f"Error_Negative_{i}"

# Solve the problem
problem.solve()

# Return the results
power_values = {j: power[j].varValue for j in range(M)}
total_error = pulp.value(problem.objective)

print(f"Optimal Power Levels: {power_values}")
print(f'Total Absolute Error: {total_error}')
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')