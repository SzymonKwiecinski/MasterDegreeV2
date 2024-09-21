import pulp

# Data from the provided JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("Power", range(data['M']), lowBound=0)  # Lamp powers
E = pulp.LpVariable.dicts("Error", range(data['N']), lowBound=0)  # Absolute errors

# Objective Function
problem += pulp.lpSum(E[i] for i in range(data['N'])), "Total_Absolute_Error"

# Constraints
for i in range(data['N']):
    actual_illumination = pulp.lpSum(data['Coefficients'][i][j] * P[j] for j in range(data['M']))
    problem += (actual_illumination - data['DesiredIlluminations'][i] <= E[i], f"Upper_Error_Constraint_{i}")
    problem += (data['DesiredIlluminations'][i] - actual_illumination <= E[i], f"Lower_Error_Constraint_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')