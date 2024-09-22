import pulp
import numpy as np

# Data in the provided format
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Number of data points
K = len(data['y'])

# Create the problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Coefficients
c = pulp.LpVariable('c', lowBound=None)  # quadratic term coefficient
b = pulp.LpVariable('b', lowBound=None)  # linear term coefficient
a = pulp.LpVariable('a', lowBound=None)  # constant term coefficient

# Auxiliary variables for absolute deviations
u = [pulp.LpVariable(f'u_{k}', lowBound=0) for k in range(K)]

# Objective function: minimize the sum of auxiliary variables
problem += pulp.lpSum(u), "Minimize_Absolute_Deviation"

# Constraints for absolute deviations
for k in range(K):
    problem += u[k] >= data['y'][k] - (c * (data['x'][k] ** 2) + b * data['x'][k] + a), f"Upper_Bound_{k}"
    problem += u[k] >= -(data['y'][k] - (c * (data['x'][k] ** 2) + b * data['x'][k] + a)), f"Lower_Bound_{k}"

# Solve the problem
problem.solve()

# Output the results
results = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(results)