import pulp
import numpy as np
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
b = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables for the center of the ball
center = [pulp.LpVariable(f'center_{i}', lowBound=None) for i in range(N)]
# Variable for the radius
radius = pulp.LpVariable('radius', lowBound=0)

# Objective: Maximize the radius
problem += radius

# Add constraints
for i in range(M):
    problem += (A[i] @ center) + radius <= b[i]
    problem += -(A[i] @ center) + radius <= b[i]

# Solve the problem
problem.solve()

# Extract the results
center_sol = [pulp.value(var) for var in center]
radius_sol = pulp.value(radius)

# Output the result
result = {
    "center": center_sol,
    "radius": radius_sol
}

print(json.dumps(result))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')