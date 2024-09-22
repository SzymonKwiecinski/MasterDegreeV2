import pulp

# Data from the provided JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']  # Number of segments
M = data['M']  # Number of lamps
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)  # Power of lamps
error = pulp.LpVariable.dicts("error", range(N), lowBound=0)  # Absolute error for segments
ill = pulp.LpVariable.dicts("illumination", range(N))  # Illumination of segments

# Objective Function: Minimize total absolute error
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Absolute_Error"

# Constraints
for i in range(N):
    # Illumination of each segment
    problem += ill[i] == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)), f"Illumination_Constraint_{i}"
    
    # Error constraints
    problem += error[i] >= ill[i] - desired_illuminations[i], f"Error_Constraint_Above_{i}"
    problem += error[i] >= desired_illuminations[i] - ill[i], f"Error_Constraint_Below_{i}"

# Solve the problem
problem.solve()

# Print the results
for j in range(M):
    print(f'Power of lamp {j}: {power[j].varValue}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')