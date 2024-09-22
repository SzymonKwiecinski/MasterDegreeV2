import json
import pulp

# Input data
data = {'NumObs': 19, 
        'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract x and y values
y_values = data['Y']
x_values = data['X']
K = len(y_values)

# Create the linear programming problem
problem = pulp.LpProblem("MinimizeMaxDeviation", pulp.LpMinimize)

# Variables for slope (b) and intercept (a)
slope = pulp.LpVariable('slope', lowBound=None)
intercept = pulp.LpVariable('intercept', lowBound=None)

# Variables for deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(K)]

# Objective: Minimize the maximum deviation
problem += pulp.lpSum(deviations)

# Constraints for deviations
for k in range(K):
    problem += deviations[k] >= y_values[k] - (slope * x_values[k] + intercept)
    problem += deviations[k] >= -(y_values[k] - (slope * x_values[k] + intercept))

# Solve the problem
problem.solve()

# Output the results
result = {
    "intercept": pulp.value(intercept),
    "slope": pulp.value(slope)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')