import pulp

# Extract data from JSON
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y = data['y']
x = data['x']
K = len(y)

# Create the problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Decision variables
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')

z_plus = [pulp.LpVariable(f'z_plus_{k}', lowBound=0, cat='Continuous') for k in range(K)]
z_minus = [pulp.LpVariable(f'z_minus_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum([z_plus[k] + z_minus[k] for k in range(K)])

# Constraints
for k in range(K):
    f_k = c * x[k]**2 + b * x[k] + a
    problem += y[k] - f_k <= z_plus[k]
    problem += f_k - y[k] <= z_minus[k]

# Solve the problem
problem.solve()

# Output the results
output = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')