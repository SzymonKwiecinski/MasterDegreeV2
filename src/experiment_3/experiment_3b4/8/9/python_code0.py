import pulp

# Data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Problem
problem = pulp.LpProblem("Illumination_Minimization", pulp.LpMinimize)

# Decision Variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0, cat='Continuous') for j in range(data['M'])]
error_plus = [pulp.LpVariable(f'error_plus_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
error_minus = [pulp.LpVariable(f'error_minus_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum([error_plus[i] + error_minus[i] for i in range(data['N'])])

# Constraints
for i in range(data['N']):
    problem += (
        pulp.lpSum([data['Coefficients'][i][j] * power[j] for j in range(data['M'])]) 
        - data['DesiredIlluminations'][i] == error_plus[i] - error_minus[i]
    )

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')