import pulp
import json

# Data from the provided JSON
data = json.loads("{'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}")

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the linear programming problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)  # Power of lamps
error = pulp.LpVariable.dicts("error", range(N), lowBound=0)  # Absolute error for segments
illumination = pulp.LpVariable.dicts("illumination", range(N), lowBound=0)  # Illumination of segments

# Objective function: minimize total absolute error
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Error"

# Constraints for illumination
for i in range(N):
    problem += illumination[i] == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)), f"Illumination_Constraint_{i}"

# Constraints for error
for i in range(N):
    problem += error[i] >= desired_illuminations[i] - illumination[i], f"Error_Constraint_Positive_{i}"
    problem += error[i] >= illumination[i] - desired_illuminations[i], f"Error_Constraint_Negative_{i}"

# Solve the problem
problem.solve()

# Output results
optimal_powers = [power[j].varValue for j in range(M)]
total_error = pulp.value(problem.objective)

print(f'Optimal Powers: {optimal_powers}')
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')