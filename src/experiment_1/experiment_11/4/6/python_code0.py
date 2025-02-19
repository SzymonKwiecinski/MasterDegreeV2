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

# Create a linear programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variable
r = pulp.LpVariable('r', lowBound=0)  # radius must be non-negative

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i, j] * r for j in range(N)) + r * np.linalg.norm(A[i]) <= B[i], f"Constraint_{i+1}")

# Objective function
problem += r, "Maximize_Radius"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')