import pulp

# Data
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = data['K']
X = data['X']
Y = data['Y']

# Define the problem
problem = pulp.LpProblem("LineFitting", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
e = [pulp.LpVariable(f'e_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(e)

# Constraints
for k in range(K):
    x_k = X[k]
    y_k = Y[k]
    
    # y_k - bx_k - a <= e_k
    problem += y_k - b * x_k - a <= e[k]
    
    # -bx_k - a + y_k <= e_k
    problem += -b * x_k - a + y_k <= e[k]

# Solve the problem
problem.solve()

# Output the results
print(f'Optimal Intercept (a): {a.varValue}')
print(f'Optimal Slope (b): {b.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')