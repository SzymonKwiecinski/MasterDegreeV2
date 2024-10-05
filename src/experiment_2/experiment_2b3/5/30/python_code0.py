import pulp

# Data from the provided JSON
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Number of data points
K = len(data['y'])

# Create the LP problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Decision variables for coefficients
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')

# Auxiliary variables for absolute deviations
abs_devs = [pulp.LpVariable(f'abs_dev_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Sum of absolute deviations
problem += pulp.lpSum(abs_devs), "Minimize_Absolute_Deviation"

# Constraints for absolute deviations
for k in range(K):
    y_k = data['y'][k]
    x_k = data['x'][k]
    predicted_y_k = c * x_k**2 + b * x_k + a
    
    # abs_devs[k] >= y_k - predicted_y_k
    problem += abs_devs[k] >= y_k - predicted_y_k
    # abs_devs[k] >= predicted_y_k - y_k
    problem += abs_devs[k] >= predicted_y_k - y_k

# Solve the problem
problem.solve()

# Output the results
output = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')