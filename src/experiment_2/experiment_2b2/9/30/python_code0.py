import pulp

# Data provided
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Extract x and y values
y_vals = data['y']
x_vals = data['x']

# The number of data points
K = len(y_vals)

# Create a linear programming problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Create variables for the coefficients of the quadratic equation
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')

# Create variables for the absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "MinimizeSumOfAbsoluteDeviations"

# Constraints: Absolute deviation definition for each data point
for k in range(K):
    y_k = y_vals[k]
    x_k = x_vals[k]
    # Absolute deviation constraints: y_k = c * x_k^2 + b * x_k + a ± deviations[k]
    problem += y_k - (c * x_k**2 + b * x_k + a) <= deviations[k]
    problem += (c * x_k**2 + b * x_k + a) - y_k <= deviations[k]

# Solve the problem
problem.solve()

# Extract the results
results = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')