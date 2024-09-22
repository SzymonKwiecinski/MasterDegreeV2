import pulp
import numpy as np
import json

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("FitBestLine", pulp.LpMinimize)

# Define the variables for slope (b) and intercept (a)
b = pulp.LpVariable("slope", lowBound=None)  
a = pulp.LpVariable("intercept", lowBound=None)

# Define the absolute deviations variables
deviations = [pulp.LpVariable(f"dev_{k}", lowBound=0) for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "Total_Deviation"

# Constraints for each data point
for k in range(K):
    problem += deviations[k] >= Y[k] - (b * X[k] + a), f"Upper_Bound_Deviation_{k}"
    problem += deviations[k] >= -(Y[k] - (b * X[k] + a)), f"Lower_Bound_Deviation_{k}"

# Solve the problem
problem.solve()

# Get the results
intercept = a.varValue
slope = b.varValue

output = {
    "intercept": intercept,
    "slope": slope
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')