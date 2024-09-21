import pulp

# Data from the provided JSON format
data = {
    'N': 3, 
    'M': 2, 
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 
    'DesiredIlluminations': [14, 3, 12]
}

# Number of illuminations and lamp powers
N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("P", range(M), lowBound=0)  # Lamp powers
E = pulp.LpVariable.dicts("E", range(N), lowBound=0)  # Absolute errors

# Objective function: minimize the sum of absolute errors
problem += pulp.lpSum(E[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    # Actual illumination minus desired must be less than or equal to the error E_i
    problem += pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i], f"Upper_Error_Constraint_{i}"
    # Desired minus actual illumination must be less than or equal to the error E_i
    problem += DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i], f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')