import pulp

# Data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Number of data points
K = len(data['x'])

# Initialize the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Decision variables
c = pulp.LpVariable('c', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)
u = pulp.LpVariable.dicts('u', range(K), lowBound=0)
v = pulp.LpVariable.dicts('v', range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([u[k] + v[k] for k in range(K)])

# Constraints
for k in range(K):
    x_k = data['x'][k]
    y_k = data['y'][k]
    problem += y_k - (c * x_k**2 + b * x_k + a) == u[k] - v[k]

# Solve the problem
problem.solve()

# Print the results
print(f'c = {c.varValue}')
print(f'b = {b.varValue}')
print(f'a = {a.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')