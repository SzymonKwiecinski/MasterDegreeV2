import pulp
import json

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Initialize the problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Create variables for coefficients a, b, c
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
c = pulp.LpVariable('c', lowBound=None)

# Create variables for absolute deviations
deviations = [pulp.LpVariable(f'dev_{i}', lowBound=0) for i in range(len(data['y']))]

# Objective function: minimize the sum of deviations
problem += pulp.lpSum(deviations)

# Constraints: y_k = c*x_k^2 + b*x_k + a +/- deviations
for k in range(len(data['y'])):
    problem += data['y'][k] == c * (data['x'][k] ** 2) + b * data['x'][k] + a + deviations[k]
    problem += data['y'][k] == c * (data['x'][k] ** 2) + b * data['x'][k] + a - deviations[k]

# Solve the problem
problem.solve()

# Retrieve the coefficients
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

# Output the result
result = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(json.dumps(result))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')