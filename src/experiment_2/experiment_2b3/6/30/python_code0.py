import pulp

# Data from JSON
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Decision variables
quadratic = pulp.LpVariable('quadratic', lowBound=-10, upBound=10)
linear = pulp.LpVariable('linear', lowBound=-10, upBound=10)
constant = pulp.LpVariable('constant', lowBound=-10, upBound=10)
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(len(data['x']))]

# Problem
problem = pulp.LpProblem("QuadraticFit", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum(deviations)

# Constraints
for k, (x_k, y_k) in enumerate(zip(data['x'], data['y'])):
    predicted_y_k = quadratic * (x_k ** 2) + linear * x_k + constant
    problem += (predicted_y_k - y_k <= deviations[k])
    problem += (y_k - predicted_y_k <= deviations[k])

# Solve
problem.solve()

# Output
output = {
    "quadratic": pulp.value(quadratic),
    "linear": pulp.value(linear),
    "constant": pulp.value(constant)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')