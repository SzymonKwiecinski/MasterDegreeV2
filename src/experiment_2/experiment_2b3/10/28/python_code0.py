import pulp

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract the values for x and y
Y = data['Y']
X = data['X']
K = data['K']

# Define the LP problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Define the variables
a = pulp.LpVariable('a', cat='Continuous')  # Intercept
b = pulp.LpVariable('b', cat='Continuous')  # Slope
e = [pulp.LpVariable(f'e_{k}', lowBound=0, cat='Continuous') for k in range(K)]  # Absolute deviations

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(e)

# Constraints
for k in range(K):
    problem += Y[k] - (a + b * X[k]) <= e[k]
    problem += Y[k] - (a + b * X[k]) >= -e[k]

# Solve the problem
problem.solve()

# Output the results
output = {
    "intercept": pulp.value(a),
    "slope": pulp.value(b)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')