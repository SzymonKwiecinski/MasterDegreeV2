import pulp
import numpy as np
import json

# Data input
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Define the Linear Program
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables for the center of the ball
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)

# Variable for the radius
r = pulp.LpVariable("r", lowBound=0)

# Objective Function: Maximize the radius r
problem += r, "Maximize Radius"

# Constraints to ensure the ball is contained within the set P
for i in range(M):
    problem += (B[i] - pulp.lpSum(A[i][j] * y[j] for j in range(N))) / np.linalg.norm(A[i]) >= r, f"Constraint_{i}"

# Solve the problem
problem.solve()

# Output results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

print(f' (Objective Value): <OBJ>{radius}</OBJ>')
print(f'Center: <CENTER>{center}</CENTER>')