import pulp
import json

# Model data in JSON format
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Parameters
y = data['y']
x = data['x']
K = len(y)
c = 1  # Assigning some value for the quadratic coefficient
b = 1  # Assigning some value for the linear coefficient
a = 0  # Assigning a value for the constant coefficient

# Create the problem
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

# Variables
z = pulp.LpVariable.dicts("z", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(z[k] for k in range(K)), "Minimize Sum of z_k"

# Constraints
for k in range(K):
    problem += z[k] >= y[k] - (c * x[k]**2 + b * x[k] + a), f"Constraint_Upper_{k}"
    problem += z[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a)), f"Constraint_Lower_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')