import pulp

# Data from the problem
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = data['K']
Y = data['Y']
X = data['X']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Absolute_Deviations", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
d_plus = pulp.LpVariable.dicts('d_plus', range(K), lowBound=0, cat='Continuous')
d_minus = pulp.LpVariable.dicts('d_minus', range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([d_plus[k] + d_minus[k] for k in range(K)])

# Constraints
for k in range(K):
    problem += d_plus[k] >= Y[k] - (b * X[k] + a)
    problem += d_minus[k] >= -(Y[k] - (b * X[k] + a))

# Solve the problem
problem.solve()

# Print the optimal values of a, b and the Objective value
print(f'a (Intercept): {pulp.value(a)}')
print(f'b (Slope): {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')