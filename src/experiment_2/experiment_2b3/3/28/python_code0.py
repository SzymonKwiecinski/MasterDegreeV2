import pulp

# Define the data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract values from the data
K = data['K']
Y = data['Y']
X = data['X']

# Create a linear programming problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Define variables for intercept and slope
intercept = pulp.LpVariable('intercept', lowBound=None, upBound=None, cat='Continuous')
slope = pulp.LpVariable('slope', lowBound=None, upBound=None, cat='Continuous')

# Define variables for the absolute deviations
d = [pulp.LpVariable(f'd_{i}', lowBound=0, upBound=None, cat='Continuous') for i in range(K)]

# Objective: Minimize the sum of absolute deviations
problem += pulp.lpSum(d)

# Constraints for absolute deviations
for i in range(K):
    problem += Y[i] - (intercept + slope * X[i]) <= d[i]
    problem += (intercept + slope * X[i]) - Y[i] <= d[i]

# Solve the problem
problem.solve()

# Output the results
output = {
    "intercept": pulp.value(intercept),
    "slope": pulp.value(slope)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')