import pulp
import json

# Data in JSON format
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

# Extracting y and x values
y_values = data['y']
x_values = data['x']
K = len(y_values)

# Create the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Variables for coefficients
c = pulp.LpVariable('c', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)

# Auxiliary variables for absolute deviation
d = [pulp.LpVariable(f'd_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the sum of deviations
problem += pulp.lpSum(d)

# Constraints for the absolute deviation
for k in range(K):
    problem += d[k] >= y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a)
    problem += d[k] >= -(y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a))

# Solve the problem
problem.solve()

# Output the coefficients
output = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')