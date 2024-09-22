import pulp
import json

# Data input
data = json.loads("{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}")

x = data['x']
y = data['y']
K = len(x)

# Create the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Variables for coefficients
c = pulp.LpVariable("c", lowBound=None)  # Coefficient for x^2
b = pulp.LpVariable("b", lowBound=None)  # Coefficient for x
a = pulp.LpVariable("a", lowBound=None)  # Constant term

# Auxiliary variables for absolute deviations
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(d[k] for k in range(K)), "Minimize_Absolute_Deviations"

# Constraints for auxiliary variables
for k in range(K):
    problem += y[k] - (c * x[k]**2 + b * x[k] + a) <= d[k], f"Upper_Bound_Constraint_{k}"
    problem += -(y[k] - (c * x[k]**2 + b * x[k] + a)) <= d[k], f"Lower_Bound_Constraint_{k}"

# Solve the problem
problem.solve()

# Output the coefficients
coefficients = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(coefficients)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')