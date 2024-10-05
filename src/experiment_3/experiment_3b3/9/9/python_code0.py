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

# Model
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Decision Variables
powers = [pulp.LpVariable(f'power_{j}', lowBound=0, cat='Continuous') for j in range(1, M + 1)]
errors = [pulp.LpVariable(f'error_{i}', lowBound=0, cat='Continuous') for i in range(1, N + 1)]

# Objective Function
problem += pulp.lpSum(errors), "Minimize_Total_Absolute_Error"

# Constraints
for i in range(N):
    illumination = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    problem += (illumination - desired_illuminations[i] <= errors[i], f"Constraint_Positive_Error_{i+1}")
    problem += (-illumination + desired_illuminations[i] <= errors[i], f"Constraint_Negative_Error_{i+1}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')