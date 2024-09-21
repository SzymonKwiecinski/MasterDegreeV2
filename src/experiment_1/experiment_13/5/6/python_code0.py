import pulp
import numpy as np

# Data from the provided JSON
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the problem variable
problem = pulp.LpProblem("Chebychev_Center_Problem", pulp.LpMaximize)

# Decision variable
r = pulp.LpVariable("r", lowBound=0)  # radius must be non-negative

# Constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])  # L2 norm of the row A[i]
    problem += (pulp.lpSum(A[i][j] * (0) for j in range(N)) + r * norm_Ai <= B[i])

# Objective function
problem += r

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')