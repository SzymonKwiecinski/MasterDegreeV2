import pulp

# Data from JSON
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

# Define decision variables
P = [pulp.LpVariable(f'P_{j}', lowBound=0, cat='Continuous') for j in range(M)]
E = [pulp.LpVariable(f'E_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective: Minimize the sum of absolute errors
problem += pulp.lpSum(E), "Total_Absolute_Error"

# Constraints
for i in range(N):
    # Sum(Coefficients[i][j] * P[j]) - DesiredIlluminations[i] <= E[i]
    problem += (pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i])
    
    # DesiredIlluminations[i] - Sum(Coefficients[i][j] * P[j]) <= E[i]
    problem += (DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i])

# Solve the problem
problem.solve()

# Output the value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')