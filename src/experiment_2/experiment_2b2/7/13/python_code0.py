import pulp
import numpy as np

# Extract data from JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the linear problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables: y_1, ..., y_N (center) and r (radius)
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective: Maximize the radius r
problem += r

# Constraints: a_i^T * y + ||a_i|| * r <= b_i
for i in range(M):
    norm_a_i = np.linalg.norm(A[i])
    problem += pulp.lpSum([A[i][j] * y[j] for j in range(N)]) + norm_a_i * r <= B[i]

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Format the output
output = {
    "center": center,
    "radius": radius
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')