import pulp

# Parse the data from the JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [
        [0.5, 0.3],
        [0.2, 0.4],
        [0.1, 0.6],
    ],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Total_Absolute_Error", pulp.LpMinimize)

# Decision variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
z_plus = [pulp.LpVariable(f'z_plus_{i}', lowBound=0) for i in range(N)]
z_minus = [pulp.LpVariable(f'z_minus_{i}', lowBound=0) for i in range(N)]

# Objective function
problem += pulp.lpSum(z_plus[i] + z_minus[i] for i in range(N))

# Constraints
for i in range(N):
    problem += (pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) + z_minus[i] - z_plus[i] 
                == desired_illuminations[i])

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')