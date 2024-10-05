import pulp
import json
import numpy as np

# Data input
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Initialize the Linear Program
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables: center (y), radius (r)
y = pulp.LpVariable.dicts("y", (range(N)), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective: Maximize the radius
problem += r, "Maximize_Radius"

# Adding constraints: a_i^T * y + |a_i| * r <= b_i
for i in range(M):
    ai = np.array(A[i])
    norm_ai = np.linalg.norm(ai)
    problem += (pulp.lpDot(ai, y) + norm_ai * r <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Format output
output = {
    "center": center,
    "radius": radius
}

# Print the output in JSON format
print(json.dumps(output, indent=4))