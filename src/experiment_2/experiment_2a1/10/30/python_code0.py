import pulp
import json

# Input Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create a linear programming problem
problem = pulp.LpProblem("Quadratic_Fitting", pulp.LpMinimize)

# Coefficients for the quadratic equation
a = pulp.LpVariable('a', lowBound=None)  # constant term
b = pulp.LpVariable('b', lowBound=None)  # linear term
c = pulp.LpVariable('c', lowBound=None)  # quadratic term

# Absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(len(data['y']))]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "Objective"

# Constraints for deviations
for k in range(len(data['y'])):
    problem += deviations[k] >= data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)
    problem += deviations[k] >= -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a))

# Solve the problem
problem.solve()

# Output the coefficients
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')