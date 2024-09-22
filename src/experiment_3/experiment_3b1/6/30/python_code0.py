import pulp
import json

# Data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Initialize the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Variables for coefficients
c = pulp.LpVariable("c", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
a = pulp.LpVariable("a", lowBound=None)

# Number of data points
K = len(data['y'])

# Auxiliary variables for absolute deviations
e = pulp.LpVariable.dicts("e", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(e[k] for k in range(K)), "Sum_of_Absolute_Deviation"

# Constraints for the absolute deviation
for k in range(K):
    problem += data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a) <= e[k]
    problem += -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)) <= e[k]

# Solve the problem
problem.solve()

# Output results
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')