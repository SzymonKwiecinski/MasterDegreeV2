import pulp
import numpy as np
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
b = np.array(data['B'])

# Create the LP problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define variables for the center of the ball
y = [pulp.LpVariable(f'y{i}', lowBound=None) for i in range(N)]

# Define the radius of the ball
r = pulp.LpVariable('r', lowBound=0)

# Define the objective function (maximize radius)
problem += r, "Maximize_radius"

# Add constraints for the ball to be within the set P
for i in range(M):
    problem += (A[i] @ np.array(y) + r <= b[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract the center and radius
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output the result
result = {
    "center": center,
    "radius": radius
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')