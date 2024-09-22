import pulp

# Data from the provided JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Error", pulp.LpMinimize)

# Decision variables for errors
error_plus = pulp.LpVariable.dicts("error_plus", range(data['N']), lowBound=0)
error_minus = pulp.LpVariable.dicts("error_minus", range(data['N']), lowBound=0)

# Decision variables for powers
power = pulp.LpVariable.dicts("power", range(data['M']), lowBound=0)

# Objective function
problem += pulp.lpSum(error_plus[i] + error_minus[i] for i in range(data['N'])), "Total_Error"

# Constraints
for i in range(data['N']):
    constraint_expr = pulp.lpSum(data['Coefficients'][i][j] * power[j] for j in range(data['M']))
    problem += constraint_expr - data['DesiredIlluminations'][i] == error_plus[i] - error_minus[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')