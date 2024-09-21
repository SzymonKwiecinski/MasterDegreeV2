import pulp

# Problem data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Extract data
N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Define the problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision variables
P = [pulp.LpVariable(f'P_{j+1}', lowBound=0) for j in range(M)]
E = [pulp.LpVariable(f'E_{i+1}', lowBound=0) for i in range(N)]

# Objective function
problem += pulp.lpSum(E), "Total_Absolute_Error"

# Constraints
for i in range(N):
    # Constraint: Coefficients * Power - DesiredIlluminations <= Error
    problem += (pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i], 
                f"Constraint_Positive_Error_{i+1}")
    
    # Constraint: DesiredIlluminations - Coefficients * Power <= Error
    problem += (DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i],
                f"Constraint_Negative_Error_{i+1}")

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')