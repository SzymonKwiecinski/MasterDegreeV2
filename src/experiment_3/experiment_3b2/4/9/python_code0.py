import pulp

# Data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Problem definition
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Variables
power = pulp.LpVariable.dicts("power", range(data['M']), lowBound=0)
e_plus = pulp.LpVariable.dicts("e_plus", range(data['N']), lowBound=0)
e_minus = pulp.LpVariable.dicts("e_minus", range(data['N']), lowBound=0)

# Objective function
problem += pulp.lpSum([e_plus[i] + e_minus[i] for i in range(data['N'])]), "Total_Error"

# Constraints
for i in range(data['N']):
    ill_i = pulp.lpSum([data['Coefficients'][i][j] * power[j] for j in range(data['M'])])
    problem += (ill_i - data['DesiredIlluminations'][i] == e_plus[i] - e_minus[i]), f"Illumination_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')