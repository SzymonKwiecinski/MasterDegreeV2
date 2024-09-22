import pulp
import json

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extracting values
K = data['K']
Y = data['Y']
X = data['X']

# Define the problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable("intercept", cat='Continuous')
b = pulp.LpVariable("slope", cat='Continuous')
deviations_positive = [pulp.LpVariable(f"d_pos_{k}", lowBound=0) for k in range(K)]
deviations_negative = [pulp.LpVariable(f"d_neg_{k}", lowBound=0) for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations_positive) + pulp.lpSum(deviations_negative)

# Constraints for absolute deviations
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= deviations_positive[k]
    problem += (b * X[k] + a) - Y[k] <= deviations_negative[k]

# Solve the problem
problem.solve()

# Extracting the intercept and slope from the solution
intercept = a.varValue
slope = b.varValue

# Output result
result = {
    "intercept": intercept,
    "slope": slope
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')