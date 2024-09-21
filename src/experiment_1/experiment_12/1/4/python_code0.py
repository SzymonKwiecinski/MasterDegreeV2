import pulp

# Extract data from the provided json format
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

# Define the Linear Programming problem
problem = pulp.LpProblem("Minimize_Absolute_Illumination_Error", pulp.LpMinimize)

# Define the decision variables: Powers (P_j) and Errors (E_i)
P = [pulp.LpVariable(f'P{j}', lowBound=0, cat='Continuous') for j in range(1, M+1)]
E = [pulp.LpVariable(f'E{i}', lowBound=0, cat='Continuous') for i in range(1, N+1)]

# Objective Function: Minimize the sum of errors
problem += pulp.lpSum(E[i] for i in range(N))

# Constraints
for i in range(N):
    # Constraint: Sum of coefficients * power - desired illumination <= error
    problem += pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i]
    # Constraint: Desired illumination - sum of coefficients * power <= error
    problem += DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')