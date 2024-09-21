import pulp

# Data from JSON
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Create the problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("Power", range(M), lowBound=0)  # P_j
E = pulp.LpVariable.dicts("Error", range(N), lowBound=0)  # E_i

# Objective Function: Minimize the sum of absolute errors
problem += pulp.lpSum(E[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    # Constraint: Actual illumination - Desired illumination <= E_i
    problem += (pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i]), f"Illumination_Upper_{i}"
    
    # Constraint: Desired illumination - Actual illumination <= E_i
    problem += (DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i]), f"Illumination_Lower_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')