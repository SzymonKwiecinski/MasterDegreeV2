import pulp
import numpy as np
import json

# Data input
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extracting values
y_values = data['Y']
x_values = data['X']
K = data['NumObs']

# Create the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable('a', lowBound=None)  # intercept
b = pulp.LpVariable('b', lowBound=None)  # slope
u = pulp.LpVariable.dicts('u', range(K), lowBound=0)  # deviations

# Objective function: Minimize the maximum deviation
problem += pulp.lpSum(u[k] for k in range(K)), "Total_Deviation"

# Constraints for each observation
for k in range(K):
    problem += y_values[k] - (b * x_values[k] + a) <= u[k]  # upper deviation
    problem += (b * x_values[k] + a) - y_values[k] <= u[k]  # lower deviation

# Solve the problem
problem.solve()

# Getting the intercept and slope
intercept = a.varValue
slope = b.varValue

# Output the results
output = {
    "intercept": intercept,
    "slope": slope
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')