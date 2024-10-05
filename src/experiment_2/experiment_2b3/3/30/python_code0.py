import pulp

# Data given
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data['y']
x_values = data['x']
K = len(y_values)

# Define the problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=-1000, upBound=1000)
b = pulp.LpVariable('b', lowBound=-1000, upBound=1000)
c = pulp.LpVariable('c', lowBound=-1000, upBound=1000)
z = [pulp.LpVariable(f'z_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(z), "MinimizeSumOfAbsoluteDeviations"

# Constraints
for k in range(K):
    y_k = y_values[k]
    x_k = x_values[k]
    problem += y_k - (c * x_k**2 + b * x_k + a) <= z[k]
    problem += (c * x_k**2 + b * x_k + a) - y_k <= z[k]

# Solve the problem
problem.solve()

# Results
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