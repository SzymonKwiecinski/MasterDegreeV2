import pulp
import json

data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = len(data['y'])
y_values = data['y']
x_values = data['x']

# Create the LP problem
problem = pulp.LpProblem("Quadratic Curve Fitting", pulp.LpMinimize)

# Define coefficients
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
c = pulp.LpVariable('c', lowBound=None)

# Define absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(K)]

# Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints for absolute deviations
for k in range(K):
    problem += deviations[k] >= y_values[k] - (c * (x_values[k] ** 2) + b * x_values[k] + a)
    problem += deviations[k] >= -(y_values[k] - (c * (x_values[k] ** 2) + b * x_values[k] + a))

# Solve the problem
problem.solve()

# Output
output = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')