import pulp

# Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

x_values = data['x']
y_values = data['y']
n = len(x_values)

# Define problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Decision variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')

# Auxiliary variables for absolute deviations
e_plus = pulp.LpVariable.dicts('e_plus', range(n), lowBound=0, cat='Continuous')
e_minus = pulp.LpVariable.dicts('e_minus', range(n), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(e_plus[k] + e_minus[k] for k in range(n))

# Constraints
for k in range(n):
    x_k = x_values[k]
    y_k = y_values[k]
    problem += y_k - (c * x_k**2 + b * x_k + a) == e_plus[k] - e_minus[k]
    problem += e_plus[k] >= 0
    problem += e_minus[k] >= 0

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')