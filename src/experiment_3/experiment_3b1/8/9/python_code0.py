import pulp

# Data from the problem statement
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

# Create the problem
problem = pulp.LpProblem("Lamp Power Optimization", pulp.LpMinimize)

# Decision variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)  # Power of each lamp
error = pulp.LpVariable.dicts("error", range(N), lowBound=0)  # Error for each segment
illumination = pulp.LpVariable.dicts("illumination", range(N), lowBound=0)  # Illumination for each segment

# Objective function: minimize the total absolute error
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Error"

# Constraints for each segment
for i in range(N):
    # Illumination constraint
    problem += illumination[i] == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)), f"Illumination_Constraint_{i}"
    
    # Error constraints
    problem += error[i] >= illumination[i] - desired_illuminations[i], f"Error_Positive_{i}"
    problem += error[i] >= desired_illuminations[i] - illumination[i], f"Error_Negative_{i}"

# Solve the problem
problem.solve()

# Print results
optimal_powers = [power[j].varValue for j in range(M)]
total_error = pulp.value(problem.objective)

print(f'Optimal Powers: {optimal_powers}')
print(f'Total Error: {total_error}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')