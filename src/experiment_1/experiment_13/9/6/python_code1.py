import pulp
import numpy as np

# Data from the JSON input
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Define the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variable
r = pulp.LpVariable("r", lowBound=0)  # radius must be non-negative

# Create decision variables for x coordinates
x_vars = [pulp.LpVariable(f"x_{j}", lowBound=None) for j in range(N)]

# Adding the constraints
for i in range(M):
    # Norm of the i-th row of A
    norm = np.linalg.norm(A[i])
    # Constraint: A[i] * x + r * norm <= B[i]
    problem += (pulp.lpSum(A[i, j] * x_vars[j] for j in range(N)) + r * norm <= B[i])

# Objective function
problem += r  # Maximize r

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')