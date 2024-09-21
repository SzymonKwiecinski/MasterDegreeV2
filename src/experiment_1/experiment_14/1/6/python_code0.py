import pulp
import numpy as np

# Define the data from the JSON
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Number of constraints and dimensions
M = data['M']
N = data['N']

# Coefficients and RHS of constraints
A = np.array(data['A'])
B = np.array(data['B'])

# Create a new Linear Programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define the decision variables
x = [pulp.LpVariable(f'x{i}', lowBound=None) for i in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective function: Maximize r
problem += r

# Constraints: Ax + r * ||A_i||_2 <= b_i for all i
for i in range(M):
    norm_A_i = np.linalg.norm(A[i])
    problem += pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * norm_A_i <= B[i]

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')