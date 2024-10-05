import pulp
import json

# Data input
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Unpacking the data
y_values = data['y']
x_values = data['x']
K = len(y_values)

# Create the LP problem
problem = pulp.LpProblem("BestQuadraticFit", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
c = pulp.LpVariable('c', cat='Continuous')
d = [pulp.LpVariable(f'd_{i}', lowBound=0, cat='Continuous') for i in range(K)]

# Objective function
problem += pulp.lpSum(d)

# Constraints
for i in range(K):
    x = x_values[i]
    y = y_values[i]
    problem += y - (c * x ** 2 + b * x + a) <= d[i]
    problem += (c * x ** 2 + b * x + a) - y <= d[i]

# Solve the problem
problem.solve()

# Output results
output = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

# Print the results in JSON format
print(json.dumps(output, indent=4))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')