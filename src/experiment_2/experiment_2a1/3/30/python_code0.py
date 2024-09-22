import pulp
import json

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Problem setup
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Variables for coefficients
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
c = pulp.LpVariable('c', lowBound=None)

# Absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(len(data['y']))]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "MinimizeAbsoluteDeviations"

# Constraints for each data point
for k in range(len(data['y'])):
    problem += deviations[k] >= data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)
    problem += deviations[k] >= -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a))

# Solve the problem
problem.solve()

# Prepare output
output = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

# Print the results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')