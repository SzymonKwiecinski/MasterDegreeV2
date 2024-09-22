import pulp
import json

# Data input
data = json.loads('{"N": 3, "M": 2, "Coefficients": [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], "DesiredIlluminations": [14, 3, 12]}')
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Define the decision variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)
e_plus = pulp.LpVariable.dicts("E_plus", range(N), lowBound=0)
e_minus = pulp.LpVariable.dicts("E_minus", range(N), lowBound=0)

# Objective function: Minimize the sum of e_i^+ and e_i^-
problem += pulp.lpSum(e_plus[i] + e_minus[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    problem += (pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) + e_minus[i] - e_plus[i] 
                 == desired_illuminations[i]), f"Illumination_Constraint_{i + 1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')