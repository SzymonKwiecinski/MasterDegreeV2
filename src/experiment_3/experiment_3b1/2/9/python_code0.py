import pulp

# Define the data from the provided JSON format
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

# Create the LP problem
problem = pulp.LpProblem("Minimize_Absolute_Error", pulp.LpMinimize)

# Decision Variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)  # Power of lamps
ill = pulp.LpVariable.dicts("ill", range(N))  # Illumination of segments
error = pulp.LpVariable.dicts("error", range(N), lowBound=0)  # Absolute error

# Objective Function
problem += pulp.lpSum(error[i] for i in range(N)), "Total_Absolute_Error"

# Constraints for illumination
for i in range(N):
    problem += ill[i] == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)), f"Illumination_Constraint_{i+1}"

# Constraints for absolute error
for i in range(N):
    problem += error[i] >= desired_illuminations[i] - ill[i], f"Error_Upper_Constraint_{i+1}"
    problem += error[i] >= ill[i] - desired_illuminations[i], f"Error_Lower_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')