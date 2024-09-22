import pulp

# Data from the provided JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Parameters
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the problem
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision Variables: Power of each lamp
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Objective Function: Minimize the total absolute error
illuminations = [pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) for i in range(N)]
errors = [pulp.lpSum(illuminations[i] - desired_illuminations[i]) for i in range(N)]

# The objective is to minimize the total absolute error
problem += pulp.lpSum(pulp.lpAbs(errors[i]) for i in range(N)), "Total_Absolute_Error"

# Solve the problem
problem.solve()

# Collecting the results
optimal_powers = [pulp.value(power[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

# Output results
print(f'Optimal Powers: {optimal_powers}')
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')