import pulp

# Data provided
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision variables
P = [pulp.LpVariable(f'P_{j+1}', lowBound=0, cat='Continuous') for j in range(M)]
E = [pulp.LpVariable(f'E_{i+1}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective function
problem += pulp.lpSum(E[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    problem += (pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i]), f"Constraint_Positive_Error_{i+1}"
    problem += (DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i]), f"Constraint_Negative_Error_{i+1}"

# Solve the problem
problem.solve()

# Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for j in range(M):
    print(f'Power of lamp {j+1} (P_{j+1}): {pulp.value(P[j])}')
for i in range(N):
    print(f'Absolute error for illumination {i+1} (E_{i+1}): {pulp.value(E[i])}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')