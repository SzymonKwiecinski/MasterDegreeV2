import pulp

# Define data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

y_values = data['y']
x_values = data['x']
K = len(y_values)

# Create the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define the variables
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
abs_deviation = [pulp.LpVariable(f'abs_dev_{i}', lowBound=0, cat='Continuous') for i in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(abs_deviation)

# Constraints for absolute deviations
for i in range(K):
    predicted_y = c * x_values[i]**2 + b * x_values[i] + a
    problem += y_values[i] - predicted_y <= abs_deviation[i]
    problem += predicted_y - y_values[i] <= abs_deviation[i]

# Solve the problem
problem.solve()

# Output the results
output = {
    'quadratic': pulp.value(c),
    'linear': pulp.value(b),
    'constant': pulp.value(a)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')