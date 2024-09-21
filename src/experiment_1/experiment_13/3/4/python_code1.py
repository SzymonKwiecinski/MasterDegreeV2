import pulp
import json

# Data
data_json = '''{"N": 3, "M": 2, "Coefficients": [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], "DesiredIlluminations": [14, 3, 12]}'''
data = json.loads(data_json)

N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Problem definition
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("Power", range(M), lowBound=0)
E = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(E[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    # Constraint for upper bound
    problem += (pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i], f"UpperBound_Constraint_{i}")
    # Constraint for lower bound
    problem += (DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i], f"LowerBound_Constraint_{i}")

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')