import pulp

# Data from JSON
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Parameters
N = data['N']  # Number of different illuminations
M = data['M']  # Number of lamp powers
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Problem
problem = pulp.LpProblem("Minimize_Illumination_Deviation", pulp.LpMinimize)

# Decision Variables
P = [pulp.LpVariable(f'P_{j}', lowBound=0, cat='Continuous') for j in range(M)]
E = [pulp.LpVariable(f'E_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective
problem += pulp.lpSum(E[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    problem += (pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i]), f'Illumination_Constraint_Pos_{i}'
    problem += (DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i]), f'Illumination_Constraint_Neg_{i}'

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')