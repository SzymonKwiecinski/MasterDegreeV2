import pulp
import json

# Given data in JSON format
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

# Extract data points
x = data['x']
y = data['y']
K = len(y)

# Create LP problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Decision variables
c = pulp.LpVariable("c", lowBound=None)  # Coefficient for x^2
b = pulp.LpVariable("b", lowBound=None)  # Coefficient for x
a = pulp.LpVariable("a", lowBound=None)  # Constant term
v = [pulp.LpVariable(f"v_{k}", lowBound=0) for k in range(K)]  # Auxiliary variables for absolute deviations

# Objective function: minimize sum of v_k
problem += pulp.lpSum(v), "MinimizeAbsoluteDeviations"

# Constraints
for k in range(K):
    problem += v[k] >= y[k] - (c * (x[k] ** 2) + b * x[k] + a), f"UpperBound_{k}"
    problem += v[k] >= - (y[k] - (c * (x[k] ** 2) + b * x[k] + a)), f"LowerBound_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')