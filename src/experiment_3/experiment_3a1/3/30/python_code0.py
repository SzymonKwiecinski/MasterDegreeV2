import pulp
import json

# Data from the provided JSON
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')
y_values = data['y']
x_values = data['x']

# Define the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define variables
c = pulp.LpVariable("c", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
a = pulp.LpVariable("a", lowBound=None)
u = [pulp.LpVariable(f"u_{k}", lowBound=0) for k in range(len(y_values))]

# Objective function
problem += pulp.lpSum(u), "Minimize_Sum_of_Absolute_Deviations"

# Constraints
for k in range(len(y_values)):
    problem += u[k] >= y_values[k] - (c * (x_values[k] ** 2) + b * x_values[k] + a), f"Constraint_Positive_{k+1}")
    problem += u[k] >= -(y_values[k] - (c * (x_values[k] ** 2) + b * x_values[k] + a)), f"Constraint_Negative_{k+1}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
# Output the coefficients
print(f'Coefficient c: {pulp.value(c)}')
print(f'Coefficient b: {pulp.value(b)}')
print(f'Coefficient a: {pulp.value(a)}')