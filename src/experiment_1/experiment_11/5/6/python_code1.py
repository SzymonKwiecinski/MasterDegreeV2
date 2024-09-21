import pulp
import numpy as np

# Data from JSON format
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create a problem variable
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define the decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=None) for j in range(N)]
r = pulp.LpVariable("r", lowBound=0)  # r must be non-negative

# Add the constraints
for i in range(M):
    # Compute the L2 norm of the i-th row of A
    norm_Ai = np.linalg.norm(A[i])
    problem += (np.dot(A[i], x) + r * norm_Ai <= B[i]), f"constraint_{i+1}"

# Objective function
problem += r, "Objective"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')