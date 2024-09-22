import pulp
import numpy as np

# Data from JSON format
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Number of data points
K = len(data['y'])

# Create the problem variable
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define variables
c = pulp.LpVariable("c", lowBound=None)  # quadratic coefficient
b = pulp.LpVariable("b", lowBound=None)  # linear coefficient
a = pulp.LpVariable("a", lowBound=None)  # constant coefficient
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]  # deviations

# Objective function
problem += pulp.lpSum(d), "Minimize_Absolute_Deviation"

# Constraints
for k in range(K):
    problem += d[k] >= data['y'][k] - (c * (data['x'][k] ** 2) + b * data['x'][k] + a), f"Upper_Bound_Constraint_{k}"
    problem += d[k] >= -(data['y'][k] - (c * (data['x'][k] ** 2) + b * data['x'][k] + a)), f"Lower_Bound_Constraint_{k}"

# Solve the problem
problem.solve()

# Output the coefficients
quadratic = c.varValue
linear = b.varValue
constant = a.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f' Quadratic Coefficient (c): {quadratic}')
print(f' Linear Coefficient (b): {linear}')
print(f' Constant Coefficient (a): {constant}')