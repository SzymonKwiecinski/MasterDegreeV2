import pulp
import numpy as np
import json

# Data from JSON
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')

# Parameters
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=None) for j in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective Function
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    ai = np.array(A[i])
    norm_ai = np.linalg.norm(ai, 2)
    constraint = pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * norm_ai
    problem += constraint <= B[i], f'Constraint_{i}'

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')