import pulp
import json

# Data input
data_json = "{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}"
data = json.loads(data_json.replace("'", "\""))

y = data['y']
x = data['x']
K = len(y)

# Problem definition
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Variables
c = pulp.LpVariable("c", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
a = pulp.LpVariable("a", lowBound=None)
z = pulp.LpVariable.dicts("z", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(z[k] for k in range(K))

# Constraints
for k in range(K):
    problem += z[k] >= y[k] - (c * x[k]**2 + b * x[k] + a)
    problem += z[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a))

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Coefficients: c={c.varValue}, b={b.varValue}, a={a.varValue}')