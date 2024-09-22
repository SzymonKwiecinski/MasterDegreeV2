import pulp
import numpy as np
import json

# Given data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
A = data['A']
b = data['B']
N = data['N']
M = data['M']

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center_Problem", pulp.LpMaximize)

# Variables representing the center of the ball (y)
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
# Variables representing the radius of the ball (r)
r = pulp.LpVariable('r', lowBound=0)

# Objective Function: Maximize the radius r
problem += r

# Constraints to ensure that the ball is within the set P
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= b[i] - r)
    problem += (pulp.lpSum(-A[i][j] * y[j] for j in range(N)) <= -b[i] + r)

# Solve the problem
problem.solve()

# Getting the result
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Print the output in the required format
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')