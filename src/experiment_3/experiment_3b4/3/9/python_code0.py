import pulp

# Extract data from the JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired = data['DesiredIlluminations']

# Create LP Problem
problem = pulp.LpProblem("Minimize_Total_Absolute_Error", pulp.LpMinimize)

# Define variables
power = pulp.LpVariable.dicts("Power", (j for j in range(M)), lowBound=0, cat='Continuous')
error = pulp.LpVariable.dicts("Error", (i for i in range(N)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(error[i] for i in range(N)), "Total Absolute Error"

# Constraints
for i in range(N):
    problem += (pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) - error[i] == desired[i]), f"Illumination_Constraint_Negative_{i}"
    problem += (pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) + error[i] == desired[i]), f"Illumination_Constraint_Positive_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')