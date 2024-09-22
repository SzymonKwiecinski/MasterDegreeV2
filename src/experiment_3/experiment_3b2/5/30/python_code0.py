import pulp
import json

# Data input
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

# Create the linear programming problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Variables for coefficients
c = pulp.LpVariable("c", lowBound=None)  # Coefficient of x^2
b = pulp.LpVariable("b", lowBound=None)  # Coefficient of x
a = pulp.LpVariable("a", lowBound=None)  # Constant term

# Variables for absolute deviations
K = len(data['y'])
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]  # Absolute deviation

# Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(d), "TotalAbsoluteDeviation"

# Constraints for each data point
for k in range(K):
    problem += data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a) <= d[k], f"UpperBoundConstraint_{k}"
    problem += (c * data['x'][k]**2 + b * data['x'][k] + a) - data['y'][k] <= d[k], f"LowerBoundConstraint_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')