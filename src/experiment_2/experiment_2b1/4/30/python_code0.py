import pulp
import json

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Variables
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
c = pulp.LpVariable('c', lowBound=None)
deviations = [pulp.LpVariable(f'deviation_{i}', lowBound=0) for i in range(len(data['y']))]

# Problem definition
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum(deviations)

# Constraints for absolute deviations
for k in range(len(data['y'])):
    problem += deviations[k] >= data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)
    problem += deviations[k] >= -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a))

# Solve the problem
problem.solve()

# Output results
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')