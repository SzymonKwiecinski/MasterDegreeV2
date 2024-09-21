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

# Initialize the problem
problem = pulp.LpProblem("ChebyshevCenter", pulp.LpMaximize)

# Decision variable for the radius
r = pulp.LpVariable('r', lowBound=0)

# Adding the constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])  # Calculating the Euclidean norm of row i
    problem += (pulp.lpSum(A[i][j] * r for j in range(N)) <= B[i] - r * norm_Ai)

# Objective function: Maximize r
problem += r

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')