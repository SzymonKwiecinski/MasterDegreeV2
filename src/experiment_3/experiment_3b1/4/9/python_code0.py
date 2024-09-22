import pulp
import json

# Data
data = json.loads("{'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}")
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Problem Definition
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Variables
powers = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Illumination errors
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(errors[i] for i in range(N)), "Total_Error"

# Constraints
for i in range(N):
    illumination_expr = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    problem += illumination_expr - desired_illuminations[i] == errors[i], f"Error_constraint_{i}"

# Solve Problem
problem.solve()

# Output
powers_values = [pulp.value(powers[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_error}</OBJ>')
print(f'Power values: {powers_values}')