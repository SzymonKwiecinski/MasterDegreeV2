import pulp
import numpy as np

# Data from JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Problem
problem = pulp.LpProblem("Maximize_Ball_Radius", pulp.LpMaximize)

# Variables
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective
problem += r, "Maximize the radius"

# Constraints
for i in range(M):
    a_i = A[i]
    b_i = B[i]
    a_i_norm = np.linalg.norm(a_i, ord=2)
    problem += pulp.lpSum(a_i[j] * y[j] for j in range(N)) + a_i_norm * r <= b_i, f"constraint_{i}"

# Solve
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')