import pulp
import json

# Data input
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')
y_values = data['y']
x_values = data['x']
K = len(y_values)

# Create the LP problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Define variables
c = pulp.LpVariable("c", cat='Continuous')
b = pulp.LpVariable("b", cat='Continuous')
a = pulp.LpVariable("a", cat='Continuous')

# Slack variables for absolute deviations
u = [pulp.LpVariable(f"u_{k}", lowBound=0) for k in range(K)]
v = [pulp.LpVariable(f"v_{k}", lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(u[k] + v[k] for k in range(K))

# Constraints
for k in range(K):
    problem += u[k] - v[k] == y_values[k] - (c * x_values[k] ** 2 + b * x_values[k] + a)

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Quadratic coefficient (c): {pulp.value(c)}')
print(f'Linear coefficient (b): {pulp.value(b)}')
print(f'Constant term (a): {pulp.value(a)}')