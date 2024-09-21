import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
r = pulp.LpVariable("r", lowBound=0)  # Radius must be non-negative
x_vars = [pulp.LpVariable(f"x_{j}") for j in range(N)]  # Variables for x

# Constraints
for i in range(M):
    # The L2 norm of each row in A
    norm_Ai = np.linalg.norm(A[i])
    problem += (pulp.lpSum(A[i, j] * x_vars[j] for j in range(N)) + r * norm_Ai <= B[i]), f"Constraint_{i}"

# Objective function
problem += r, "Objective"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>') 