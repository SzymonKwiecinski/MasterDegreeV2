import pulp
import numpy as np
import json

# Given data in JSON format
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y = data['y']
x = data['x']
K = len(y)

# Create the LP problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define the coefficients for the quadratic equation
c = pulp.LpVariable('c', lowBound=None)  # coefficient of x^2
b = pulp.LpVariable('b', lowBound=None)  # coefficient of x
a = pulp.LpVariable('a', lowBound=None)  # constant term

# Define the absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(K)]

# Define the objective function
problem += pulp.lpSum(deviations), "Objective"

# Constraints for deviations
for k in range(K):
    problem += deviations[k] >= y[k] - (c * x[k]**2 + b * x[k] + a)
    problem += deviations[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a))

# Solve the problem
problem.solve()

# Extracting the coefficients
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output format
output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

# Print the result
print(json.dumps(output, indent=4))