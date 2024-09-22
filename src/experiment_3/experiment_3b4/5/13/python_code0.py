import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, upBound=None, cat='Continuous')

# Objective
problem += r

# Constraints
for i in range(M):
    norm_ai = np.linalg.norm(A[i])
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + norm_ai * r <= B[i])

# Solve
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')