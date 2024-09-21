import pulp
import numpy as np

# Data from the JSON input
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Define the Linear Programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), cat=pulp.LpContinuous)
r = pulp.LpVariable("r", lowBound=0, cat=pulp.LpContinuous)  # r >= 0

# Objective function: Maximize r
problem += r, "Maximize radius of Chebychev center"

# Constraints
for i in range(M):
    constraint_expr = pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * np.linalg.norm(A[i], 2)
    problem += constraint_expr <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
print(f"Status: {pulp.LpStatus[problem.status]}")
for j in range(N):
    print(f"x[{j}] = {pulp.value(x[j])}")
print(f"r (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")