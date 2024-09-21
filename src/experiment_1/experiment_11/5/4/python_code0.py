import pulp

# Data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Number of illuminations and lamp powers
N = data['N']
M = data['M']

# Coefficients and desired illuminations
Coefficients = data['Coefficients']
DesiredIlluminations = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("LampPower", range(M), lowBound=0)  # Lamp powers
E = pulp.LpVariable.dicts("Error", range(N), lowBound=0)      # Absolute errors

# Objective Function
problem += pulp.lpSum(E[i] for i in range(N)), "Objective"

# Constraints
for i in range(N):
    # Constraint for upper bound of error
    problem += (pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) - DesiredIlluminations[i] <= E[i])
    # Constraint for lower bound of error
    problem += (DesiredIlluminations[i] - pulp.lpSum(Coefficients[i][j] * P[j] for j in range(M)) <= E[i])

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')