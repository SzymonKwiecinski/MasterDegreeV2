import pulp
import json

data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("Linear_Regression", pulp.LpMinimize)

# Variables for the intercept (a) and slope (b)
a = pulp.LpVariable("intercept", lowBound=None)
b = pulp.LpVariable("slope", lowBound=None)

# Absolute deviations
deviations = [pulp.LpVariable(f"dev_{k}", lowBound=0) for k in range(K)]

# Objective Function: Minimize the sum of deviations
problem += pulp.lpSum(deviations)

# Constraints for absolute deviations
for k in range(K):
    problem += deviations[k] >= Y[k] - (b * X[k] + a)
    problem += deviations[k] >= -(Y[k] - (b * X[k] + a))

# Solve the problem
problem.solve()

# Obtain the intercept and slope
intercept = a.varValue
slope = b.varValue

# Output the results
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')