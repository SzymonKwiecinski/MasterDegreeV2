import pulp

# Data from JSON
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Create the problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("P", range(data['M']), lowBound=0)  # Lamp powers
E = pulp.LpVariable.dicts("E", range(data['N']), lowBound=0)  # Absolute errors

# Objective Function
problem += pulp.lpSum(E[i] for i in range(data['N'])), "Total_Absolute_Error"

# Constraints
for i in range(data['N']):
    problem += (pulp.lpSum(data['Coefficients'][i][j] * P[j] for j in range(data['M'])) - data['DesiredIlluminations'][i] <= E[i]), f"Upper_Error_Constraint_{i}"
    problem += (data['DesiredIlluminations'][i] - pulp.lpSum(data['Coefficients'][i][j] * P[j] for j in range(data['M'])) <= E[i]), f"Lower_Error_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')