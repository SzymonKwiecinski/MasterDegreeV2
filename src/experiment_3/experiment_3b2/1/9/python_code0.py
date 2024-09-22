import pulp
import json

# Given data in JSON format
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

# Extract data
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)
error_positive = pulp.LpVariable.dicts("Error_Positive", range(N), lowBound=0)
error_negative = pulp.LpVariable.dicts("Error_Negative", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(error_positive[i] + error_negative[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    problem += (
        pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) + error_positive[i] - error_negative[i] == desired[i],
        f"Constraint_{i}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')