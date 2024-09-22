import pulp
import json

# Data input
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Create the linear programming problem
problem = pulp.LpProblem("LineFitting", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable("intercept", lowBound=None)
b = pulp.LpVariable("slope", lowBound=None)
M = pulp.LpVariable("max_deviation", lowBound=0)

# Define the constraints
for k in range(data['NumObs']):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    problem += y_k - (b * x_k + a) <= M  # d_k <= M
    problem += -(y_k - (b * x_k + a)) <= M  # -d_k <= M

# Set the objective function
problem += M  # Minimize M

# Solve the problem
problem.solve()

# Print the results
intercept = a.varValue
slope = b.varValue
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Intercept: {intercept}, Slope: {slope}')