import pulp

# Data from JSON format
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Extracting data
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the linear programming problem
problem = pulp.LpProblem("RoadIlluminationOptimization", pulp.LpMinimize)

# Decision variables for lamp powers
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)

# Calculate the illumination for each segment
illumination = pulp.LpVariable.dicts("illumination", range(N))

# Objective function: minimize the absolute error
error = pulp.LpVariable("error", lowBound=0)
problem += error

# Constraints for illumination and error
for i in range(N):
    # Illumination calculation using the coefficients
    problem += illumination[i] == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    # Absolute error constraints
    problem += illumination[i] - desired_illuminations[i] <= error
    problem += - (illumination[i] - desired_illuminations[i]) <= error

# Solve the problem
problem.solve()

# Output results
lamp_powers = [power[j].varValue for j in range(M)]
total_error = pulp.value(error)

print(f'Lamp Powers: {lamp_powers}')
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')