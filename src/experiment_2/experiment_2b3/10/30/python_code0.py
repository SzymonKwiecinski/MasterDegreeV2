import pulp

# Data from the problem
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Extract x and y values
x_values = data['x']
y_values = data['y']
K = len(x_values)

# Define the linear programming problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Define variables for coefficients a, b, c
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')

# Define variables for absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints for deviations
for k in range(K):
    x_k = x_values[k]
    y_k = y_values[k]
    predicted_y_k = c * (x_k**2) + b * x_k + a
    problem += deviations[k] >= y_k - predicted_y_k
    problem += deviations[k] >= predicted_y_k - y_k

# Solve the problem
problem.solve()

# Collect the results
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')