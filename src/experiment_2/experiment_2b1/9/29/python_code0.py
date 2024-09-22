import pulp
import json

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Number of observations
K = data['NumObs']
y_values = data['Y']
x_values = data['X']

# Create the LP problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable("intercept", lowBound=None)  # intercept
b = pulp.LpVariable("slope", lowBound=None)      # slope
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(K)]

# Objective function: minimize the maximum deviation
problem += pulp.lpSum(deviations)

# Constraints: yi = bx + a + deviation for each observation
for k in range(K):
    problem += deviations[k] >= y_values[k] - (b * x_values[k] + a), f"Upper_Bound_{k}"
    problem += deviations[k] >= -(y_values[k] - (b * x_values[k] + a)), f"Lower_Bound_{k}"

# Solve the problem
problem.solve()

# Retrieve results
intercept = a.varValue
slope = b.varValue

# Output result
result = {
    "intercept": intercept,
    "slope": slope
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')