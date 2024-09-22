import pulp

# Define the data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Problem definition
problem = pulp.LpProblem("MinimizeIlluminationError", pulp.LpMinimize)

# Variables
power = pulp.LpVariable.dicts("power", range(data['M']), lowBound=0)  # Power of lamps
error = pulp.LpVariable.dicts("error", range(data['N']), lowBound=0)  # Error for segments
ill = pulp.LpVariable.dicts("ill", range(data['N']), lowBound=0)      # Illumination for segments

# Objective function: Minimize the sum of errors
problem += pulp.lpSum(error[i] for i in range(data['N'])), "TotalError"

# Constraints
for i in range(data['N']):
    # Calculate illumination
    problem += ill[i] == pulp.lpSum(data['Coefficients'][i][j] * power[j] for j in range(data['M'])), f"IlluminationCalculation_{i}"
    
    # Error constraints
    problem += -error[i] <= ill[i] - data['DesiredIlluminations'][i], f"LowerErrorBound_{i}"
    problem += ill[i] - data['DesiredIlluminations'][i] <= error[i], f"UpperErrorBound_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')