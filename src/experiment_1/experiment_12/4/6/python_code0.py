import pulp
import numpy as np

# Data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Linear Programming Problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')  # radius
x = [pulp.LpVariable(f'x{i}', cat='Continuous') for i in range(N)]  # center coordinates

# Objective
problem += r, "Maximize radius"

# Constraints
for i in range(M):
    norm_A_i = np.linalg.norm(A[i])
    constraint_expr = pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * norm_A_i
    problem += (constraint_expr <= B[i], f"Constraint_{i}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')