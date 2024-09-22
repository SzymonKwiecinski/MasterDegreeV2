import pulp
import json

# Data input
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

y = data['y']
x = data['x']
K = len(y)

# Create the optimization problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define the decision variables
c = pulp.LpVariable("c", cat="Continuous")
b = pulp.LpVariable("b", cat="Continuous")
a = pulp.LpVariable("a", cat="Continuous")
z = [pulp.LpVariable(f"z_{k}", lowBound=0, cat="Continuous") for k in range(K)]

# Objective function
problem += pulp.lpSum(z)

# Constraints
for k in range(K):
    problem += z[k] >= y[k] - (c * x[k]**2 + b * x[k] + a)
    problem += z[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a))

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')