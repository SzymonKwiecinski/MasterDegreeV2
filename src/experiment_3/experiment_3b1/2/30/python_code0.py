import pulp
import json

# Input Data
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')
x_values = data['x']
y_values = data['y']
K = len(x_values)

# Define the problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Define decision variables
c = pulp.LpVariable("c", None)  # Coefficient for x^2
b = pulp.LpVariable("b", None)  # Coefficient for x
a = pulp.LpVariable("a", None)  # Constant term
t = pulp.LpVariable.dicts("t", range(K), lowBound=0)  # Auxiliary variables

# Objective function
problem += pulp.lpSum(t[k] for k in range(K)), "TotalAbsoluteDeviation"

# Constraints
for k in range(K):
    problem += t[k] >= y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a), f"UpperBoundConstraint_k{_}"
    problem += t[k] >= -(y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a)), f"LowerBoundConstraint_k{_}"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Coefficients: c = {c.varValue}, b = {b.varValue}, a = {a.varValue}')