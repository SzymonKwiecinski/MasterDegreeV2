import pulp
import json

# Given data in JSON format
data = '''{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'''
data = json.loads(data)

# Extracting the variables from data
y_values = data['y']
x_values = data['x']
K = len(y_values)

# Creating the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable("a", LowBound=None)  # coefficient of constant
b = pulp.LpVariable("b", LowBound=None)  # coefficient of linear term
c = pulp.LpVariable("c", LowBound=None)  # coefficient of quadratic term
d = pulp.LpVariable.dicts("d", range(K), lowBound=0)  # absolute deviations

# Objective function
problem += pulp.lpSum(d[k] for k in range(K)), "Minimize_Absolute_Deviation"

# Constraints
for k in range(K):
    problem += d[k] >= y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a), f"Upper_Bound_Deviation_{k}"
    problem += d[k] >= -(y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a)), f"Lower_Bound_Deviation_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')