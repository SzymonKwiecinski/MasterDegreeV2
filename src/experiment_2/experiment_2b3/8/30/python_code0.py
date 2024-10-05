import pulp

# Data input
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y = data['y']
x = data['x']
K = len(y)

# Define the problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Define the variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')

# Define slack variables for absolute deviations
d = [pulp.LpVariable(f'd_{k}', cat='Continuous') for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(d)

# Constraints to model absolute deviations
for k in range(K):
    problem += y[k] - (c * x[k]**2 + b * x[k] + a) <= d[k]
    problem += -(y[k] - (c * x[k]**2 + b * x[k] + a)) <= d[k]

# Solve the problem
problem.solve()

# Extract the values of a, b, c
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

# Output the results
output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')