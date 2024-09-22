import pulp

# Data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Initialize the problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Create decision variables
power = pulp.LpVariable.dicts("power", range(data['M']), lowBound=0)
e = pulp.LpVariable.dicts("e", range(data['N']), lowBound=0)

# Objective function: Minimize the total absolute error
problem += pulp.lpSum(e[i] for i in range(data['N'])), "Total_Absolute_Error"

# Constraints
for i in range(data['N']):
    # Illumination calculation
    ill_i = pulp.lpSum(data['Coefficients'][i][j] * power[j] for j in range(data['M']))
    
    # Absolute error constraints
    problem += e[i] >= ill_i - data['DesiredIlluminations'][i], f"Error_Positive_{i}"
    problem += e[i] >= data['DesiredIlluminations'][i] - ill_i, f"Error_Negative_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')