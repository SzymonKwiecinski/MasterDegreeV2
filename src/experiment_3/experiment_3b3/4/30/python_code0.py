import pulp

# Extract x and y from data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
y_data = data['y']
x_data = data['x']
K = len(y_data)

# Create the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define variables for coefficients and deviations
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Define objective function to minimize the sum of deviations
problem += pulp.lpSum(d)

# Add constraints for absolute deviations
for k in range(K):
    x_k = x_data[k]
    y_k = y_data[k]
    # Add constraints for each k
    problem += y_k - (c * x_k**2 + b * x_k + a) <= d[k]
    problem += -(y_k - (c * x_k**2 + b * x_k + a)) <= d[k]

# Solve the problem
problem.solve()

# Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'c (quadratic coefficient): {pulp.value(c)}')
print(f'b (linear coefficient): {pulp.value(b)}')
print(f'a (constant term): {pulp.value(a)}')