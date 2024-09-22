import pulp

# Given data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

y = data['y']
x = data['x']
K = len(y)

# Define the problem
problem = pulp.LpProblem('QuadraticCurveFitting', pulp.LpMinimize)

# Define decision variables
c = pulp.LpVariable('c', lowBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(d)

# Constraints
for k in range(K):
    predicted = c * (x[k] ** 2) + b * x[k] + a
    problem += d[k] >= y[k] - predicted
    problem += d[k] >= -(y[k] - predicted)

# Solve the problem
problem.solve()

# Collect results
quadratic_coefficient = pulp.value(c)
linear_coefficient = pulp.value(b)
constant_coefficient = pulp.value(a)

# Output results
output = {
    "quadratic": quadratic_coefficient,
    "linear": linear_coefficient,
    "constant": constant_coefficient
}

# Objective value
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')