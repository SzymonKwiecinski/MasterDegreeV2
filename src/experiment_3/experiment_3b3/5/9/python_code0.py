import pulp

# Read the input data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create a problem instance
problem = pulp.LpProblem("LampPowerOptimization", pulp.LpMinimize)

# Decision variables for the power of lamps
power_vars = [pulp.LpVariable(f'power_{j+1}', lowBound=0, cat='Continuous') for j in range(M)]

# Decision variables for the error (positive and negative)
e_plus_vars = [pulp.LpVariable(f'e_plus_{i+1}', lowBound=0, cat='Continuous') for i in range(N)]
e_minus_vars = [pulp.LpVariable(f'e_minus_{i+1}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective function: Minimize the sum of positive and negative errors
problem += pulp.lpSum([e_plus_vars[i] + e_minus_vars[i] for i in range(N)]), "TotalError"

# Constraints for each segment
for i in range(N):
    # Illumination equation
    illum_i = pulp.lpSum([coefficients[i][j] * power_vars[j] for j in range(M)])
    
    # Error terms constraints
    problem += e_plus_vars[i] >= illum_i - desired_illuminations[i], f"constraint_e_plus_{i+1}"
    problem += e_minus_vars[i] >= desired_illuminations[i] - illum_i, f"constraint_e_minus_{i+1}"

# Solve the problem
problem.solve()

# Output the results
power = [pulp.value(var) for var in power_vars]
error = pulp.value(problem.objective)
print(f'(Power Values): {power}')
print(f' (Objective Value): <OBJ>{error}</OBJ>')