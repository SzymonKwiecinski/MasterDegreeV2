import pulp
import json

# Input data from JSON format
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
Y = data['Y']
X = data['X']
K = data['NumObs']

# Create a linear programming problem
problem = pulp.LpProblem("Linear_Regression_Problem", pulp.LpMinimize)

# Decision variables for slope (b) and intercept (a)
b = pulp.LpVariable("slope", lowBound=None)
a = pulp.LpVariable("intercept", lowBound=None)

# Decision variables for deviations
deviations_pos = [pulp.LpVariable(f"deviation_pos_{k}", lowBound=0) for k in range(K)]
deviations_neg = [pulp.LpVariable(f"deviation_neg_{k}", lowBound=0) for k in range(K)]

# Objective function: minimize the maximum deviation
problem += pulp.lpSum(deviations_pos) + pulp.lpSum(deviations_neg)

# Constraints for each observation
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= deviations_pos[k]
    problem += (b * X[k] + a) - Y[k] <= deviations_neg[k]

# Solve the problem
problem.solve()

# Intercept and slope values
intercept = a.varValue
slope = b.varValue

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the results
result = {
    "intercept": intercept,
    "slope": slope
}

print(result)