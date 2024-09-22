import pulp

# Input data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

y_values = data['y']
x_values = data['x']
K = len(y_values)

# Problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
c = pulp.LpVariable('c', cat='Continuous')

# Absolute deviations
deviation = [pulp.LpVariable(f'dev_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize sum of absolute deviations
problem += pulp.lpSum(deviation), "Minimize_Absolute_Deviation"

# Constraints
for k in range(K):
    y_k = y_values[k]
    x_k = x_values[k]
    problem += y_k - (c * (x_k ** 2) + b * x_k + a) <= deviation[k]
    problem += (c * (x_k ** 2) + b * x_k + a) - y_k <= deviation[k]

# Solve the problem
problem.solve()

# Extract solution
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

# Output
output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')