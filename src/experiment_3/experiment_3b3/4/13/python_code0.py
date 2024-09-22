import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Problem
problem = pulp.LpProblem("Maximize_Ball_Radius", pulp.LpMaximize)

# Variables
y = [pulp.LpVariable(f'y_{i}', lowBound=None, cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r <= B[i], f"Constraint_{i}"

# Solve
problem.solve()

# Extracting solution
center = [pulp.value(y_i) for y_i in y]
radius = pulp.value(r)

# Output
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')