import pulp
import json

# Data in JSON format
data = json.loads('{"N": 3, "M": 2, "Coefficients": [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], "DesiredIlluminations": [14, 3, 12]}')

# Parameters
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the problem variable
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)
illumination = pulp.LpVariable.dicts("Illumination", range(N), lowBound=0)
error = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(error[i] for i in range(N))

# Constraints for illumination
for i in range(N):
    problem += illumination[i] == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)), f"Illumination_Constraint_{i}"

# Constraints for error handling
for i in range(N):
    problem += error[i] >= illumination[i] - desired_illuminations[i], f"Positive_Error_Constraint_{i}"
    problem += error[i] >= desired_illuminations[i] - illumination[i], f"Negative_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')