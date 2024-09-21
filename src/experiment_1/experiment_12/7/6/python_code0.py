import pulp
import numpy as np

# Problem data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=None, cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective: Maximize r
problem += r, "MaximizeRadius"

# Constraints
norms_A = np.linalg.norm(A, axis=1)

for i in range(M):
    problem += (pulp.lpDot(A[i], x) + r * norms_A[i] <= B[i]), f'Constraint_{i+1}'

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')