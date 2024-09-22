import numpy as np
import pulp
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables for the center of the ball
center = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
radius = pulp.LpVariable('r', lowBound=0)

# Objective function: maximize the radius
problem += radius

# Constraints: for each linear inequality
for i in range(M):
    problem += (A[i, :].dot(center) + radius <= B[i])

# Solve the problem
problem.solve()

# Extract results
center_result = [pulp.value(c) for c in center]
radius_result = pulp.value(radius)

# Output results
output = {
    "center": center_result,
    "radius": radius_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')