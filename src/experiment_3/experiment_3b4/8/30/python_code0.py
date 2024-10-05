import pulp

# Data from JSON
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y = data['y']
x = data['x']
K = len(y)

# Create a Linear Programming problem
problem = pulp.LpProblem("Quadratic_Fit_Error_Minimization", pulp.LpMinimize)

# Decision Variables
e_plus = [pulp.LpVariable(f'e_plus_{k}', lowBound=0) for k in range(K)]
e_minus = [pulp.LpVariable(f'e_minus_{k}', lowBound=0) for k in range(K)]
c = pulp.LpVariable('c')
b = pulp.LpVariable('b')
a = pulp.LpVariable('a')

# Objective Function
problem += pulp.lpSum([e_plus[k] + e_minus[k] for k in range(K)])

# Constraints
for k in range(K):
    problem += y[k] - (c * x[k]**2 + b * x[k] + a) == e_plus[k] - e_minus[k]

# Solve the problem
problem.solve()

# Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')