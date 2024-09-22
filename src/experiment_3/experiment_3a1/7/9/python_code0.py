import pulp

# Data from the provided JSON
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision variables
power = pulp.LpVariable.dicts("power", range(data['M']), lowBound=0)  # power_j
error_pos = pulp.LpVariable.dicts("error_pos", range(data['N']), lowBound=0)  # error_i^+
error_neg = pulp.LpVariable.dicts("error_neg", range(data['N']), lowBound=0)  # error_i^-

# Objective function: Minimize the total absolute error
problem += pulp.lpSum(error_pos[i] + error_neg[i] for i in range(data['N'])), "Total_Absolute_Error"

# Constraints for illumination and error
for i in range(data['N']):
    # Calculate illumination
    ill_i = pulp.lpSum(data['Coefficients'][i][j] * power[j] for j in range(data['M']))
    
    # Constraints for the absolute error representation
    problem += error_pos[i] >= ill_i - data['DesiredIlluminations'][i], f"Error_Pos_Constraint_{i}"
    problem += error_neg[i] >= data['DesiredIlluminations'][i] - ill_i, f"Error_Neg_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')