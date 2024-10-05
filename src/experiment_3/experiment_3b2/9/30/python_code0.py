import pulp
import json

# Data provided in JSON format
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Extracting x and y values from data
x_values = data['x']
y_values = data['y']
K = len(x_values)

# Initialize the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
c = pulp.LpVariable('c', lowBound=None)
d = [pulp.LpVariable(f'd_{k}', lowBound=0) for k in range(K)]

# Objective Function
problem += pulp.lpSum(d)

# Constraints
for k in range(K):
    problem += d[k] >= y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a)
    problem += d[k] >= -(y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')