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

# Create the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variable
r = pulp.LpVariable("r", lowBound=0)

# Constraints
for i in range(M):
    # Norm of the i-th row of A
    norm_Ai = np.linalg.norm(A[i])
    problem += (A[i, :].dot(pulp.LpVariable("x", 0, None, pulp.LpContinuous)) + r * norm_Ai <= B[i]), f"Constraint_{i+1}"

# Objective
problem += r

# Solve the problem
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')