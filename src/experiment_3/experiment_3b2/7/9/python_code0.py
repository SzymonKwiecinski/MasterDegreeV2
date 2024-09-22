import pulp

# Data extracted from the provided JSON format
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
problem = pulp.LpProblem("Minimize_Absolute_Errors", pulp.LpMinimize)

# Define the decision variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)  # power variables (non-negative)
errors = pulp.LpVariable.dicts("error", range(N), lowBound=0)  # error variables (non-negative)

# Objective function
problem += pulp.lpSum(errors[i] for i in range(N)), "Minimize_Total_Error"

# Illumination constraints and error constraints
for i in range(N):
    # Calculate actual illumination for segment i
    illumination = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    
    # Illumination constraint
    problem += illumination == desired_illuminations[i], f"Illumination_Constraint_{i}"
    
    # Absolute error constraints
    problem += illumination - desired_illuminations[i] <= errors[i], f"Error_Upper_{i}"
    problem += desired_illuminations[i] - illumination <= errors[i], f"Error_Lower_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')