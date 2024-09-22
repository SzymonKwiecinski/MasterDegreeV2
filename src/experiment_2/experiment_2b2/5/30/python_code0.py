import pulp

# Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Variables
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')

# Absolute Deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0, cat='Continuous') for k in range(len(data['y']))]

# Objective Function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints: y[k] predicted = c * x[k]^2 + b * x[k] + a
for k in range(len(data['y'])):
    x_k = data['x'][k]
    y_k = data['y'][k]
    problem += y_k - (c * x_k**2 + b * x_k + a) <= deviations[k]
    problem += (c * x_k**2 + b * x_k + a) - y_k <= deviations[k]

# Solve the problem
problem.solve()

# Output
output = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')