import pulp

# Extract data from JSON
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}
y_values = data['y']
x_values = data['x']
K = len(y_values)

# Initialize the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
z = [pulp.LpVariable(f'z_{k}', lowBound=0, upBound=None, cat='Continuous') for k in range(K)]

# Objective function: Minimize the sum of z_k
problem += pulp.lpSum(z), "Objective"

# Constraints
for k in range(K):
    x_k = x_values[k]
    y_k = y_values[k]
    # z_k >= y_k - (c * x_k^2 + b * x_k + a)
    problem += z[k] >= y_k - (c * x_k**2 + b * x_k + a)
    # z_k >= -(y_k - (c * x_k^2 + b * x_k + a))
    problem += z[k] >= -(y_k - (c * x_k**2 + b * x_k + a))

# Solve the problem
problem.solve()

# Print results
objective_value = pulp.value(problem.objective)
print(f'(Objective Value): <OBJ>{objective_value}</OBJ>')
print(f'Quadratic term (c): {c.varValue}')
print(f'Linear term (b): {b.varValue}')
print(f'Constant term (a): {a.varValue}')