import pulp

# Data from provided JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Extracting data
N = data['N']
M = data['M']
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("P", range(M), lowBound=0)  # Power of lamps
E = pulp.LpVariable.dicts("E", range(N), lowBound=0)  # Absolute errors

# Objective Function
problem += pulp.lpSum(E[i] for i in range(N)), "TotalAbsoluteError"

# Constraints
for i in range(N):
    problem += pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i], f"ErrorConstraint_Lower_{i}"
    problem += DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i], f"ErrorConstraint_Upper_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')