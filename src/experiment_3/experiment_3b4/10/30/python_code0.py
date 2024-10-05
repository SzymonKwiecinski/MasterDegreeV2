import pulp

# Data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Number of data points
K = len(data['y'])

# Problem
problem = pulp.LpProblem("Quadratic_Fitting", pulp.LpMinimize)

# Variables
c = pulp.LpVariable('c', lowBound=-1000, upBound=1000, cat='Continuous')
b = pulp.LpVariable('b', lowBound=-1000, upBound=1000, cat='Continuous')
a = pulp.LpVariable('a', lowBound=-1000, upBound=1000, cat='Continuous')
z = [pulp.LpVariable(f'z_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective
problem += pulp.lpSum(z)

# Constraints
for k in range(K):
    x_k = data['x'][k]
    y_k = data['y'][k]
    problem += z[k] >= y_k - (c * x_k**2 + b * x_k + a)
    problem += z[k] >= -(y_k - (c * x_k**2 + b * x_k + a))

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')