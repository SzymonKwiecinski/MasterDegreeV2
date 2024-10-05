import pulp
import json

# Data
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')
y_values = data['y']
x_values = data['x']
K = len(y_values)

# Problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Variables
c = pulp.LpVariable('c', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(K)]

# Objective Function
problem += pulp.lpSum(deviations)

# Constraints
for k in range(K):
    x_k = x_values[k]
    y_k = y_values[k]
    problem += deviations[k] >= y_k - (c * x_k ** 2 + b * x_k + a)
    problem += deviations[k] >= -(y_k - (c * x_k ** 2 + b * x_k + a))

# Solve
problem.solve()

# Result
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')