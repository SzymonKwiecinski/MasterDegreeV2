import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Initiate the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
r = pulp.LpVariable('r', lowBound=0)  # Radius
x = pulp.LpVariable.dicts('x', range(N))  # Chebychev center coordinates

# Objective: Maximize the radius r
problem += r, "Maximize_Radius"

# Constraints
for i in range(M):
    # Calculate the L2 norm of the i-th row of A
    A_i_norm = np.linalg.norm(A[i, :])
    # Add the constraint: A[i] * x + r * norm(A[i]) <= B[i]
    constraint = pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * A_i_norm
    problem += (constraint <= B[i], f"Constraint_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')