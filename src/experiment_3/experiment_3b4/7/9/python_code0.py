import pulp

# Problem data
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

# Create a linear programming problem
problem = pulp.LpProblem("OptimalLampPower", pulp.LpMinimize)

# Decision variables
powers = pulp.LpVariable.dicts("Power", range(M), lowBound=0, cat='Continuous')
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0, cat='Continuous')

# Objective function: Minimize total absolute error
problem += pulp.lpSum(errors[i] for i in range(N)), "Total Absolute Error"

# Constraints
for i in range(N):
    illumination_i = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    # Error constraints
    problem += errors[i] >= illumination_i - desired_illuminations[i]
    problem += errors[i] >= desired_illuminations[i] - illumination_i

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')