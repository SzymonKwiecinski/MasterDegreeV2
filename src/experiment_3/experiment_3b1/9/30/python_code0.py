import pulp
import json

# Input data
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Extracting x and y values
x_values = data['x']
y_values = data['y']
K = len(x_values)

# Create the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Decision variables
c = pulp.LpVariable('c', lowBound=None)  # Coefficient of x^2
b = pulp.LpVariable('b', lowBound=None)  # Coefficient of x
a = pulp.LpVariable('a', lowBound=None)  # Constant term
t = pulp.LpVariable.dicts('t', range(K), lowBound=0)  # Slack variables

# Objective function
problem += pulp.lpSum(t[k] for k in range(K)), "Total_Absolute_Deviation"

# Constraints
for k in range(K):
    problem += y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a) <= t[k], f"Upper_Bound_Constraint_{k}"
    problem += -(y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a)) <= t[k], f"Lower_Bound_Constraint_{k}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f' Coefficients: a = {a.varValue}, b = {b.varValue}, c = {c.varValue}')