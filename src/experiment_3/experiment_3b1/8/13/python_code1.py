import pulp
import numpy as np

# Data from the provided JSON format
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)  # Center
r = pulp.LpVariable("r", lowBound=0)  # Radius

# Objective function
problem += r, "Objective"

# Constraints
for i in range(M):
    a_i = A[i]
    b_i = B[i]
    norm_a_i = np.linalg.norm(a_i)
    problem += r <= (np.dot(a_i, [y[j] for j in range(N)]) - b_i) / norm_a_i, f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the center and the radius
center = np.array([pulp.value(y[j]) for j in range(N)])
radius = pulp.value(r)

print(f' (Objective Value): <OBJ>{radius}</OBJ>')
print(f'Center: {center}')