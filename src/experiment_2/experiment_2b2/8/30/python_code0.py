import pulp

# Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data['y']
x_values = data['x']
K = len(y_values)

# Problem
problem = pulp.LpProblem("Curve_Fit_Quadratic", pulp.LpMinimize)

# Decision Variables
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function: Minimize sum of absolute deviations
problem += pulp.lpSum(d), "Minimize_Deviation"

# Constraints
for k in range(K):
    # Absolute value deviations constraint
    problem += y_values[k] - (c * (x_values[k] ** 2) + b * x_values[k] + a) <= d[k]
    problem += (c * (x_values[k] ** 2) + b * x_values[k] + a) - y_values[k] <= d[k]

# Solve
problem.solve()

# Output results
results = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')