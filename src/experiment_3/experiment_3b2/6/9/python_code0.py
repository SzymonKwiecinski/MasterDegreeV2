import pulp

# Data from the provided JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Problem definition
problem = pulp.LpProblem("OptimalLampPower", pulp.LpMinimize)

# Variable definitions
powers = pulp.LpVariable.dicts("power", range(data['M']), lowBound=0)  # power_j >= 0
errors = pulp.LpVariable.dicts("error", range(data['N']), lowBound=0)  # error_i >= 0

# Objective function
problem += pulp.lpSum(errors[i] for i in range(data['N']))

# Constraints for illumination calculation and absolute error
for i in range(data['N']):
    illumination = pulp.lpSum(data['Coefficients'][i][j] * powers[j] for j in range(data['M']))
    problem += illumination - data['DesiredIlluminations'][i] <= errors[i]
    problem += data['DesiredIlluminations'][i] - illumination <= errors[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')