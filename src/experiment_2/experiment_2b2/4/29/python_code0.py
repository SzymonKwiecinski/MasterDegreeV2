import pulp

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Define the LP problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Decision variables for slope, intercept and maximum deviation
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
max_dev = pulp.LpVariable('max_dev', lowBound=0, cat='Continuous')

# The objective function: minimize the maximum deviation
problem += max_dev

# Add constraints for each data point
for i in range(data['NumObs']):
    y_k = data['Y'][i]
    x_k = data['X'][i]
    # deviation constraints
    problem += a + b * x_k - y_k <= max_dev
    problem += y_k - (a + b * x_k) <= max_dev

# Solve the problem
problem.solve()

# Retrieve the results
intercept = pulp.value(a)
slope = pulp.value(b)

# Output the results
output = {
    "intercept": intercept,
    "slope": slope
}

print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
print(output)