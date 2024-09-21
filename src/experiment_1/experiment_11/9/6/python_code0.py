import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
b = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variable
r = pulp.LpVariable("r", lowBound=0)  # Radius must be non-negative

# Adding constraints
for i in range(M):
    norm_A_i = np.linalg.norm(A[i])
    problem += (A[i, :].dot(np.array([1] * N))) + r * norm_A_i <= b[i], f"Constraint_{i+1}"

# Objective function
problem += r, "Objective"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')