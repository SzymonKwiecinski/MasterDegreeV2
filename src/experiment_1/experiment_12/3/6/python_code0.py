import pulp
import numpy as np

# Data from JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Parameters
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the LP problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective: Maximize the radius r
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    Ai_norm = np.linalg.norm(A[i])
    problem += pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * Ai_norm <= B[i], f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')