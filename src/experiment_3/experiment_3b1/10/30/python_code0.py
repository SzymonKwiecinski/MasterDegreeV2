import pulp
import json

# Input data
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

x_values = data['x']
y_values = data['y']
K = len(x_values)

# Create the model
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define variables
c = pulp.LpVariable("c", lowBound=None)  # Coefficient of x^2
b = pulp.LpVariable("b", lowBound=None)  # Coefficient of x
a = pulp.LpVariable("a", lowBound=None)  # Constant term
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]  # Deviations

# Objective function
problem += pulp.lpSum(d[k] for k in range(K)), "Total_Absolute_Deviation"

# Constraints
for k in range(K):
    problem += d[k] >= y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a), f"Upper_Bound_Constraint_{k}"
    problem += d[k] >= -(y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a)), f"Lower_Bound_Constraint_{k}"

# Solve the problem
problem.solve()

# Output the coefficients
print(f'Quadratic Coefficient (c): {c.varValue}')
print(f'Linear Coefficient (b): {b.varValue}')
print(f'Constant Coefficient (a): {a.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')