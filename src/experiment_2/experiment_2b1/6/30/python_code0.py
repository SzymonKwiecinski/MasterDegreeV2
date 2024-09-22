import pulp
import json

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create the Linear Programming problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
c = pulp.LpVariable("c", lowBound=None)

# Define the deviation variables
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(len(data['y']))]

# Objective function: Minimize the sum of deviations
problem += pulp.lpSum(deviations)

# Constraints: absolute deviations
for k in range(len(data['y'])):
    predicted = c * (data['x'][k] ** 2) + b * data['x'][k] + a
    problem += predicted - data['y'][k] <= deviations[k]
    problem += data['y'][k] - predicted <= deviations[k]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')