import pulp

# Data
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = data['K']
Y = data['Y']
X = data['X']

# Define the problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Variables
b = pulp.LpVariable('b', lowBound=-10, upBound=10, cat='Continuous')
a = pulp.LpVariable('a', lowBound=-10, upBound=10, cat='Continuous')
u = [pulp.LpVariable(f'u_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(u[k] for k in range(K))

# Constraints
for k in range(K):
    problem += u[k] >= Y[k] - (b * X[k] + a)
    problem += u[k] >= -(Y[k] - (b * X[k] + a))

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')