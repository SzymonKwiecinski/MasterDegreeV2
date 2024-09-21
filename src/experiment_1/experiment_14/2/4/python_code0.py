import pulp

# Data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Define the problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision Variables
P = [pulp.LpVariable(f'P_{j+1}', lowBound=0, cat='Continuous') for j in range(data['M'])]
E = [pulp.LpVariable(f'E_{i+1}', lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum(E[i] for i in range(data['N']))

# Constraints
for i in range(data['N']):
    # Constraint: Actual illumination should not exceed desired by more than E_i
    problem += pulp.lpSum(data['Coefficients'][i][j] * P[j] for j in range(data['M'])) - data['DesiredIlluminations'][i] <= E[i], f"Constraint1_Illumination_{i+1}"

    # Constraint: Desired illumination should not exceed actual by more than E_i
    problem += data['DesiredIlluminations'][i] - pulp.lpSum(data['Coefficients'][i][j] * P[j] for j in range(data['M'])) <= E[i], f"Constraint2_Illumination_{i+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')