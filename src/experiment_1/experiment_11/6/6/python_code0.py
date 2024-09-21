import pulp
import numpy as np

# Data from JSON format
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

# Create the problem
problem = pulp.LpProblem("Chebychev_Center_Problem", pulp.LpMaximize)

# Define the decision variable
r = pulp.LpVariable("r", lowBound=0)

# Add the constraints
for i in range(M):
    problem += (r * np.linalg.norm(A[i]) <= B[i] - pulp.lpSum(A[i][j] * pulp.LpVariable(f'x_{j}') for j in range(N)), f"constraint_{i}")

# Set the objective function
problem += r, "Objective"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')