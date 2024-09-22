import pulp
import numpy as np
import json

data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract Y and X values
Y = data['Y']
X = data['X']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Define variables for slope (b) and intercept (a)
b = pulp.LpVariable("b", lowBound=None)  # Slope
a = pulp.LpVariable("a", lowBound=None)  # Intercept

# Define variables for the deviations
deviation_pos = [pulp.LpVariable(f'dev_pos_{k}', lowBound=0) for k in range(len(Y))]
deviation_neg = [pulp.LpVariable(f'dev_neg_{k}', lowBound=0) for k in range(len(Y))]

# Objective function: minimize the maximum deviation
max_deviation = pulp.LpVariable("max_deviation", lowBound=0)
problem += max_deviation

# Constraints to ensure deviations represent the differences
for k in range(len(Y)):
    problem += Y[k] - (b * X[k] + a) <= max_deviation + deviation_neg[k]
    problem += -(Y[k] - (b * X[k] + a)) <= max_deviation + deviation_pos[k]

# Solve the problem
problem.solve()

# Retrieve the results
intercept = a.varValue
slope = b.varValue

# Output the results
result = {
    "intercept": intercept,
    "slope": slope
}

print(json.dumps(result))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')