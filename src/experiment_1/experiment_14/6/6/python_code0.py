import pulp
import numpy as np
import json

# Data from JSON
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')

M = data['M']
N = data['N']
A = np.array(data['A'])
b = np.array(data['B'])

# Create the linear programming problem
problem = pulp.LpProblem("Find_Chebychev_Center", pulp.LpMaximize)

# Decision variables: Chebychev center coordinates (x) and radius (r)
x = [pulp.LpVariable(f'x{i}', lowBound=None, cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective function: Maximize the radius r
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])
    problem += pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * norm_Ai <= b[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')