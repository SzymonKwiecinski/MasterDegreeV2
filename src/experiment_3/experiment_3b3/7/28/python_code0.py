import pulp

# Data
data = {'K': 19, 
        'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Create a linear programming problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

# Decision Variables
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
d = pulp.LpVariable.dicts('d', range(K), lowBound=0, cat='Continuous')

# Objective
problem += pulp.lpSum([d[k] for k in range(K)]), "Objective"

# Constraints
for k in range(K):
    problem += d[k] >= Y[k] - (b * X[k] + a), f"Constraint1_{k}"
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"Constraint2_{k}"

# Solve the problem
problem.solve()

# Output the results
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')