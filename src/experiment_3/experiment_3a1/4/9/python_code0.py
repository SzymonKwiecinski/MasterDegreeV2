import pulp
import json

data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Create the LP problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

# Decision variables
power = pulp.LpVariable.dicts("Power", range(M), lowBound=0)

# Auxiliary variables for absolute errors
errors = pulp.LpVariable.dicts("Error", range(N), lowBound=0)

# Objective function: minimize sum of errors
problem += pulp.lpSum(errors[i] for i in range(N))

# Constraints for illumination calculation and error
for i in range(N):
    ill_i = pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    # Actual illumination
    problem += ill_i == pulp.lpSum(coefficients[i][j] * power[j] for j in range(M))
    # Error constraints
    problem += errors[i] >= ill_i - desired_illuminations[i]
    problem += errors[i] >= desired_illuminations[i] - ill_i

# Solve the problem
problem.solve()

# Output results
powers = [power[j].value() for j in range(M)]
total_error = pulp.value(problem.objective)

print(f' (Power Values): {powers}')
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')