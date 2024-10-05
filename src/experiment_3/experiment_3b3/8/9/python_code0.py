import pulp

# Parse the data
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}
N = data['N']
M = data['M']
coeff = data['Coefficients']
desired = data['DesiredIlluminations']

# Create the LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Define variables
power = [pulp.LpVariable(f'power_{j}', lowBound=0, cat='Continuous') for j in range(M)]
error = [pulp.LpVariable(f'error_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective function: Minimize the sum of absolute errors
problem += pulp.lpSum(error[i] for i in range(N))

# Constraints
for i in range(N):
    illum_expr = pulp.lpSum(coeff[i][j] * power[j] for j in range(M))
    problem += illum_expr - desired[i] <= error[i]
    problem += desired[i] - illum_expr <= error[i]

# Solve the problem
problem.solve()

# Output the results
print("Optimal Power Settings:")
for j in range(M):
    print(f"power_{j}: {pulp.value(power[j])}")

print("Errors for each segment:")
for i in range(N):
    print(f"error_{i}: {pulp.value(error[i])}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')