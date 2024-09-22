import pulp

# Data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

x_values = data['x']
y_values = data['y']
K = len(x_values)

# Problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Decision variables
c = pulp.LpVariable('c', lowBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')

u = [pulp.LpVariable(f'u_{k}', lowBound=0, cat='Continuous') for k in range(K)]
v = [pulp.LpVariable(f'v_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum([u[k] + v[k] for k in range(K)])

# Constraints
for k in range(K):
    x_k = x_values[k]
    y_k = y_values[k]
    
    problem += u[k] - v[k] == y_k - (c * x_k**2 + b * x_k + a)

# Solve
problem.solve()

# Output results
print(f'Coefficients: {{ "quadratic": {c.varValue}, "linear": {b.varValue}, "constant": {a.varValue} }}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')