import pulp
import json

# Input data
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

y = data['y']
x = data['x']
K = len(y)

# Create a linear programming problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Decision variables
c = pulp.LpVariable("c", lowBound=None)  # Coefficient for x^2
b = pulp.LpVariable("b", lowBound=None)  # Coefficient for x
a = pulp.LpVariable("a", lowBound=None)  # Constant term
z = [pulp.LpVariable(f"z_{k}", lowBound=0) for k in range(K)]  # Absolute deviations

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(z)

# Constraints
for k in range(K):
    problem += z[k] >= y[k] - (c * x[k]**2 + b * x[k] + a)
    problem += z[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a))

# Solve the problem
problem.solve()

# Output the results
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')