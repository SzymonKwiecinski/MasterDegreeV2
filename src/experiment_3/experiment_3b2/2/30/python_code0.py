import pulp
import numpy as np
import json

# Input data in JSON format
data = json.loads("{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}")

# Extract data
y = data['y']
x = data['x']
K = len(y)

# Create the problem
problem = pulp.LpProblem("Minimize_Deviation", pulp.LpMinimize)

# Decision Variables
c = pulp.LpVariable("c", lowBound=None)  # Coefficient of x^2
b = pulp.LpVariable("b", lowBound=None)  # Coefficient of x
a = pulp.LpVariable("a", lowBound=None)  # Constant coefficient
d = pulp.LpVariable.dicts("d", range(K), lowBound=0)  # Deviation variables

# Objective function
problem += pulp.lpSum(d[k] for k in range(K)), "Total_Deviation"

# Constraints
for k in range(K):
    problem += y[k] - (c * x[k]**2 + b * x[k] + a) <= d[k], f"Constraint_1_{k+1}"
    problem += (c * x[k]**2 + b * x[k] + a) - y[k] <= d[k], f"Constraint_2_{k+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')