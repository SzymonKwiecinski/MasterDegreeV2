import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M, N = data['M'], data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective function
problem += r

# Constraints
for i in range(M):
    norm_ai = np.linalg.norm(A[i])
    problem += pulp.lpSum([A[i][j] * y[j] for j in range(N)]) + r * norm_ai <= B[i]

# Solve
problem.solve()

# Output
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)
print(f'Center: {center}')
print(f'Radius: {radius}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')