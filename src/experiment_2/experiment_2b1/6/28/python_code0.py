import pulp
import json

# Given data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Number of data points
K = data['K']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Variables for the slope (b) and intercept (a)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)

# Variables for the absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the sum of deviations
problem += pulp.lpSum(deviations)

# Constraints for the deviations
for k in range(K):
    problem += deviations[k] >= Y[k] - (b * X[k] + a)
    problem += deviations[k] >= -(Y[k] - (b * X[k] + a))

# Solve the problem
problem.solve()

# Output the results
intercept = a.varValue
slope = b.varValue

output = {
    "intercept": intercept,
    "slope": slope
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')