import pulp

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data["y"]
x_values = data["x"]
n = len(y_values)

# Initialize the LP problem
problem = pulp.LpProblem("Quadratic_Fitting", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('constant', lowBound=None)
b = pulp.LpVariable('linear', lowBound=None)
c = pulp.LpVariable('quadratic', lowBound=None)

# Variables for absolute deviation
deviations = [pulp.LpVariable(f'dev_{i}', lowBound=0) for i in range(n)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints for each data point
for i in range(n):
    problem += deviations[i] >= y_values[i] - (c * x_values[i]**2 + b * x_values[i] + a)
    problem += deviations[i] >= -(y_values[i] - (c * x_values[i]**2 + b * x_values[i] + a))

# Solve the problem
problem.solve()

# Collect results
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

# Print results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')