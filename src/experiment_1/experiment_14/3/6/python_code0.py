import pulp
import numpy as np
import json

# Load data from JSON
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create a linear programming problem to maximize r
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x{i}', lowBound=None) for i in range(N)]  # x vector
r = pulp.LpVariable('r', lowBound=0)  # radius, non-negative

# Objective function: Maximize r
problem += r, "Objective: Maximize_r"

# Constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])
    problem += pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * norm_Ai <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract and print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(N):
    print(f'x[{i}]: {pulp.value(x[i])}')
print(f'r: {pulp.value(r)}')