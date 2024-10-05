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

# Problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
d_plus = [pulp.LpVariable(f'd_plus_{k}', lowBound=0, cat='Continuous') for k in range(K)]
d_minus = [pulp.LpVariable(f'd_minus_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum([d_plus[k] + d_minus[k] for k in range(K)])

# Constraints
for k in range(K):
    problem += (X[k] * b + a + d_plus[k] >= Y[k])
    problem += (X[k] * b + a - d_minus[k] <= Y[k])

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')