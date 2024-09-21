import pulp
import numpy as np

# Data from JSON
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
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define the decision variable
r = pulp.LpVariable("r", lowBound=0)  # Radius, must be non-negative

# Define the x variables
x = [pulp.LpVariable(f'x_{j}') for j in range(N)]

# Add constraints
for i in range(M):
    # The norm of A_i (Euclidean norm)
    norm_Ai = np.linalg.norm(A[i])
    problem += (pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * norm_Ai <= B[i])

# Objective function
problem += r  # Maximize the radius r

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')