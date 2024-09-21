import pulp
import numpy as np

# Data provided
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
b = np.array(data['B'])

# Create the linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define variables
x = [pulp.LpVariable(f'x{i}', lowBound=None) for i in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective function: Maximize r
problem += r, "Objective"

# Constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])
    problem += pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * norm_Ai <= b[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')