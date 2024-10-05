import pulp
import json
import numpy as np

# Load data
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the Linear Programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define the variables y (center) and r (radius)
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective: Maximize r
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    constraint_expr = pulp.lpSum([A[i][j] * y[j] for j in range(N)]) + r * np.linalg.norm(np.array(A[i]))
    problem += constraint_expr <= B[i], f"Inequality_constraint_{i}"

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Format output
output = {
    "center": center,
    "radius": radius
}

# Print output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')