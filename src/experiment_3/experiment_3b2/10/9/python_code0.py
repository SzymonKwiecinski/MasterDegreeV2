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

# Define the problem
problem = pulp.LpProblem("Minimize_Total_Absolute_Error", pulp.LpMinimize)

# Variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)
error = pulp.LpVariable.dicts("err", range(N), lowBound=0)
ill = pulp.LpVariable.dicts("ill", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(error[i] for i in range(N))

# Constraints
for i in range(N):
    problem += ill[i] == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))  # Illumination calculation
    problem += ill[i] - desired_illuminations[i] <= error[i]  # Upper error constraint
    problem += desired_illuminations[i] - ill[i] <= error[i]  # Lower error constraint

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')