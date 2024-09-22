import pulp
import json

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create the problem variable
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Define the coefficients a, b, c
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
c = pulp.LpVariable('c', lowBound=None)

# Create variables for absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(len(data['y']))]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints: y[k] = c*x[k]^2 + b*x[k] + a + deviations[k]
for k in range(len(data['y'])):
    problem += c * (data['x'][k] ** 2) + b * data['x'][k] + a - deviations[k] <= data['y'][k]
    problem += -deviations[k] <= c * (data['x'][k] ** 2) + b * data['x'][k] + a - data['y'][k]

# Solve the problem
problem.solve()

# Output the results
output = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')