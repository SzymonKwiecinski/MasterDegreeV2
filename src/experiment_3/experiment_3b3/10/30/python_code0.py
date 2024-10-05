import pulp

# Data from the JSON input
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Extract y and x values
y_values = data['y']
x_values = data['x']
K = len(y_values)

# Define the LP problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')
e = [pulp.LpVariable(f'e_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize sum of absolute deviations
problem += pulp.lpSum(e)

# Constraints for each data point
for k in range(K):
    x_k = x_values[k]
    y_k = y_values[k]
    # y_k - (c * x_k^2 + b * x_k + a) <= e_k
    problem += y_k - (c * (x_k ** 2) + b * x_k + a) <= e[k]
    # -(y_k - (c * x_k^2 + b * x_k + a)) <= e_k
    problem += -(y_k - (c * (x_k ** 2) + b * x_k + a)) <= e[k]

# Solve the problem
problem.solve()

# Output results
c_value = pulp.value(c)
b_value = pulp.value(b)
a_value = pulp.value(a)

print(f'(Quadratic): {c_value}, (Linear): {b_value}, (Constant): {a_value}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')