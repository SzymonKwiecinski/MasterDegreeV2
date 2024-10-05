import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Minimize_Total_Error", pulp.LpMinimize)

# Variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0) for j in range(M)]
error = [pulp.LpVariable(f'error_{i}', lowBound=0) for i in range(N)]

# Objective Function
problem += pulp.lpSum(error[i] for i in range(N))

# Constraints
for i in range(N):
    equation = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    desired = desired_illuminations[i]
    problem += equation - desired <= error[i]
    problem += -equation + desired <= error[i]

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')