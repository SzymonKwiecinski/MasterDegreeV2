import pulp

# Extract the data from the provided JSON format
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Define the problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', lowBound=None)  # Intercept
b = pulp.LpVariable('b', lowBound=None)  # Slope
d = pulp.LpVariable('d', lowBound=0)     # Maximum deviation

# Objective function
problem += d, "Minimize the maximum deviation"

# Constraints
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    # Absolute deviation constraints
    problem += y_k - (b * x_k + a) <= d
    problem += (b * x_k + a) - y_k <= d

# Solve the problem
problem.solve()

# Output the optimal intercept and slope
results = {
    "intercept": pulp.value(a),
    "slope": pulp.value(b)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')