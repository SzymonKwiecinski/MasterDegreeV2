import json
import pulp

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extracting y and x values
y_values = data['y']
x_values = data['x']
K = len(y_values)

# Create the problem
problem = pulp.LpProblem("Quadratic_Fitting", pulp.LpMinimize)

# Coefficients for the quadratic equation
a = pulp.LpVariable("a", lowBound=None)  # Constant term
b = pulp.LpVariable("b", lowBound=None)  # Linear term
c = pulp.LpVariable("c", lowBound=None)  # Quadratic term

# Variables for absolute deviations
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints for each data point
for k in range(K):
    problem += deviations[k] >= y_values[k] - (c * x_values[k] ** 2 + b * x_values[k] + a)
    problem += deviations[k] >= -(y_values[k] - (c * x_values[k] ** 2 + b * x_values[k] + a))

# Solve the problem
problem.solve()

# Output the coefficients
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')