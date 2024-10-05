import pulp

# Data input
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Define problem
problem = pulp.LpProblem("BestFitLine_MinSumOfAbsoluteDeviations", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable('intercept', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('slope', lowBound=None, upBound=None, cat='Continuous')
d = [pulp.LpVariable(f'd_{i}', lowBound=0, cat='Continuous') for i in range(K)]

# Objective function
problem += pulp.lpSum(d), "Minimize_Sum_of_Absolute_Deviations"

# Constraints
for i in range(K):
    problem += Y[i] - (a + b * X[i]) <= d[i]
    problem += (a + b * X[i]) - Y[i] <= d[i]

# Solve the problem
problem.solve()

# Get the results
intercept = pulp.value(a)
slope = pulp.value(b)

# Output result
output = {
    "intercept": intercept,
    "slope": slope
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')