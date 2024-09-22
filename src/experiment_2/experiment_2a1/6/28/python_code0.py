import pulp
import json

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Number of data points
K = data['K']

# Create the linear programming problem
problem = pulp.LpProblem("Linear_Regression", pulp.LpMinimize)

# Decision variables for slope (b) and intercept (a)
slope = pulp.LpVariable("slope", lowBound=None)
intercept = pulp.LpVariable("intercept", lowBound=None)

# Decision variables for the absolute deviations
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints for each data point
for k in range(K):
    problem += deviations[k] >= data['Y'][k] - (slope * data['X'][k] + intercept)
    problem += deviations[k] >= -(data['Y'][k] - (slope * data['X'][k] + intercept))

# Solve the problem
problem.solve()

# Extract the slope and intercept
slope_value = slope.varValue
intercept_value = intercept.varValue

# Output result
result = {
    "intercept": intercept_value,
    "slope": slope_value
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')