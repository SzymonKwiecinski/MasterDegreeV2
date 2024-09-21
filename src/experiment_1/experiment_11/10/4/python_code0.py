import pulp
import json

# Data input
data = json.loads('{"N": 3, "M": 2, "Coefficients": [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], "DesiredIlluminations": [14, 3, 12]}')

N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Create the problem variable
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("P", range(M), lowBound=0)  # Lamp powers
E = pulp.LpVariable.dicts("E", range(N), lowBound=0)  # Absolute errors

# Objective Function
problem += pulp.lpSum([E[i] for i in range(N)]), "Total_Error"

# Constraints
for i in range(N):
    # Error constraints for the ith illumination
    problem += (pulp.lpSum([Coefficients[i][j] * P[j] for j in range(M)]) - DesiredIlluminations[i] <= E[i]), f"Error_Less_Constraint_{i}"
    problem += (DesiredIlluminations[i] - pulp.lpSum([Coefficients[i][j] * P[j] for j in range(M)]) <= E[i]), f"Error_More_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')