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

# Decision variables for the center of the ball
y = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
# Decision variable for the radius
r = pulp.LpVariable('r', lowBound=0)

# Objective function: maximize the radius
problem += r

# Add constraints to ensure the ball is contained within the set P
for i in range(M):
    problem += (A[i] @ y) <= b[i] - r
    problem += (A[i] @ y) >= b[i] + r

# Solve the problem
problem.solve()

# Extract the center and radius
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Prepare output
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')