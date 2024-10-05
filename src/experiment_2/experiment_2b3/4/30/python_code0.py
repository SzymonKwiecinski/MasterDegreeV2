import pulp

# Data from the problem
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data['y']
x_values = data['x']
n = len(y_values)

# Define the LP problem
problem = pulp.LpProblem("Quadratic_Regression", pulp.LpMinimize)

# Define variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')

# Define absolute deviation variables
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(n)]

# Add constraints for absolute deviations
for k in range(n):
    y_k = y_values[k]
    x_k = x_values[k]
    problem += y_k - (c * x_k**2 + b * x_k + a) <= d[k]
    problem += -(y_k - (c * x_k**2 + b * x_k + a)) <= d[k]

# Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(d)

# Solve the problem
problem.solve()

# Retrieve the coefficients
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

# Output format
output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')