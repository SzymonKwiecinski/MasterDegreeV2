import pulp

# Data from the JSON
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Problem definition
problem = pulp.LpProblem("Illumination Minimization", pulp.LpMinimize)

# Decision Variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(data['M'])]
error_plus = [pulp.LpVariable(f'error_plus_{i}', lowBound=0) for i in range(data['N'])]
error_minus = [pulp.LpVariable(f'error_minus_{i}', lowBound=0) for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum([error_plus[i] + error_minus[i] for i in range(data['N'])])

# Constraints
for i in range(data['N']):
    # Compute illumination
    illumination = pulp.lpSum([data['Coefficients'][i][j] * power[j] for j in range(data['M'])])
    
    # Constraint: sum(coeff * power) = illumination
    problem += illumination == data['DesiredIlluminations'][i] + error_plus[i] - error_minus[i]
    
    # Constraint: errors must be non-negative
    problem += error_plus[i] >= 0
    problem += error_minus[i] >= 0

# Solve the problem
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')