import pulp

# Data input
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data['y']
x_values = data['x']
K = len(x_values)

# Define the Linear Programming problem
problem = pulp.LpProblem("Best_Quadratic_Fit", pulp.LpMinimize)

# Define decision variables
c = pulp.LpVariable('c', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)

# Add variables for absolute deviations
abs_deviation_vars = [pulp.LpVariable(f'abs_dev_{i}', lowBound=0) for i in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(abs_deviation_vars)

# Constraints for absolute deviations
for i in range(K):
    predicted_y = c * (x_values[i] ** 2) + b * x_values[i] + a
    problem += predicted_y - y_values[i] <= abs_deviation_vars[i]
    problem += y_values[i] - predicted_y <= abs_deviation_vars[i]

# Solve the problem
problem.solve()

# Extracting the coefficients
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')