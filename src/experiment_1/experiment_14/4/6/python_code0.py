import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective: Maximize r
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    Ai_norm = np.linalg.norm(A[i])
    constraint = pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * Ai_norm <= B[i]
    problem += constraint

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')