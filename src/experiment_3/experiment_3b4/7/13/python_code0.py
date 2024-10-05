import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
y_vars = [pulp.LpVariable(f'y_{i}', cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective
problem += r, "Maximize radius"

# Constraints
for i in range(M):
    a_i = np.array(A[i])
    norm_a_i = np.linalg.norm(a_i, 2)
    problem += pulp.lpSum([a_i[j] * y_vars[j] for j in range(N)]) + norm_a_i * r <= B[i], f"Constraint_{i}"

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')