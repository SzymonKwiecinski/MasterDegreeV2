import pulp
import json

data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create problem variable
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Variables for coefficients a, b, c
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
c = pulp.LpVariable('c', lowBound=None)

# Define absolute deviation variables
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(len(data['y']))]

# Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "Total_Absolute_Deviation"

# Constraints for each data point
for k in range(len(data['y'])):
    problem += deviations[k] >= data['y'][k] - (c*data['x'][k]**2 + b*data['x'][k] + a)
    problem += deviations[k] >= -(data['y'][k] - (c*data['x'][k]**2 + b*data['x'][k] + a))

# Solve the problem
problem.solve()

# Get values of coefficients
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

# Print the output
print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')