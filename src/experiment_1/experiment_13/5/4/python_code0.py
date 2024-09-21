import pulp

# Data from the provided JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("P", range(M), lowBound=0)  # Lamp powers
E = pulp.LpVariable.dicts("E", range(N), lowBound=0)  # Absolute errors

# Objective Function
problem += pulp.lpSum(E[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    problem += pulp.lpSum(coefficients[i][j] * P[j] for j in range(M)) - desired_illuminations[i] <= E[i], f"Upper_Error_Constraint_{i}"
    problem += desired_illuminations[i] - pulp.lpSum(coefficients[i][j] * P[j] for j in range(M)) <= E[i], f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')