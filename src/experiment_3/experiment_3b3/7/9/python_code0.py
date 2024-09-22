import pulp

# Extracting data from JSON
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illumination = data['DesiredIlluminations']

# Create a Linear Program
problem = pulp.LpProblem("Lamp_Power_Minimization", pulp.LpMinimize)

# Decision Variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Auxiliary Variables for Absolute Errors
errors = [pulp.LpVariable(f'error_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective Function
problem += pulp.lpSum(errors), "Total_Absolute_Error"

# Constraints
for i in range(N):
    illumination_i = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    problem += illumination_i - desired_illumination[i] <= errors[i], f"Constraint_Positive_Error_{i}"
    problem += desired_illumination[i] - illumination_i <= errors[i], f"Constraint_Negative_Error_{i}"

# Solve the problem
problem.solve()

# Printing results
for j in range(M):
    print(f'Optimal power of lamp {j+1}: {pulp.value(power[j])}')
print(f'Total Absolute Error: {pulp.value(problem.objective)} (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')