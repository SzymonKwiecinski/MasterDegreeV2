import pulp

# Data provided
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Coefficients
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')

# Absolute deviation variables
abs_dev_vars = [pulp.LpVariable(f'abs_dev_{i}', lowBound=0, cat='Continuous') for i in range(len(data['y']))]

# Objective function: Minimize sum of absolute deviations
problem += pulp.lpSum(abs_dev_vars)

# Add constraints for absolute deviations
for i, (y_k, x_k) in enumerate(zip(data['y'], data['x'])):
    problem += abs_dev_vars[i] >= y_k - (c * x_k**2 + b * x_k + a)
    problem += abs_dev_vars[i] >= -(y_k - (c * x_k**2 + b * x_k + a))

# Solve the problem
problem.solve()

# Output the results
results = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')