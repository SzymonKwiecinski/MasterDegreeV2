import pulp

# Data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
c = pulp.LpVariable('c', cat='Continuous')
e = pulp.LpVariable.dicts('e', range(len(data['x'])), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(e)

# Constraints
for k in range(len(data['x'])):
    x_k = data['x'][k]
    y_k = data['y'][k]
    # Linearize absolute deviations
    problem += y_k - (c * x_k ** 2 + b * x_k + a) <= e[k]
    problem += (c * x_k ** 2 + b * x_k + a) - y_k <= e[k]

# Solve the problem
problem.solve()

# Print the results
print(f"(a, b, c): ({pulp.value(a)}, {pulp.value(b)}, {pulp.value(c)})")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')