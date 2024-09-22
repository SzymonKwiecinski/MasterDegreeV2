import pulp
import json

# Data provided
data = json.loads('{"N": 3, "M": 2, "Coefficients": [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], "DesiredIlluminations": [14, 3, 12]}')

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define decision variables for lamp powers
powers = pulp.LpVariable.dicts("power", range(M), lowBound=0)

# Define error variables
z = pulp.LpVariable.dicts("z", range(N), lowBound=0)
w = pulp.LpVariable.dicts("w", range(N), lowBound=0)

# Define the objective function
problem += pulp.lpSum(z[i] + w[i] for i in range(N))

# Define the constraints
for i in range(N):
    # Compute illumination
    problem += z[i] - w[i] == pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M)) - desired_illuminations[i], f"Illumination_Constraint_{i}"

    # Ensure z_i is greater than or equal to the positive error
    problem += z[i] >= pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M)) - desired_illuminations[i], f"Positive_Error_Constraint_{i}"

    # Ensure w_i is greater than or equal to the absolute negative error
    problem += w[i] >= - (pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M)) - desired_illuminations[i]), f"Negative_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
lamp_powers = {j: powers[j].varValue for j in range(M)}
objective_value = pulp.value(problem.objective)

print(f'Lamp Powers: {lamp_powers}')
print(f' (Objective Value): <OBJ>{objective_value}</OBJ>')