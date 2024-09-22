import pulp
import numpy as np

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
b = np.array(data['B'])

# Create the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define variables
y = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
r = pulp.LpVariable("r", lowBound=0)

# Objective function: maximize the radius
problem += r

# Constraints for each inequality a_i^T y <= b_i - r
for i in range(M):
    problem += (A[i, :] @ y) <= b[i] - r
    problem += (-A[i, :] @ y) <= b[i] + r

# Solve the problem
problem.solve()

# Extracting results
center = [pulp.value(y_j) for y_j in y]
radius = pulp.value(r)

# Output the result
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')