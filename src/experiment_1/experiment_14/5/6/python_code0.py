import pulp
import numpy as np

# Parse the given data
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

# Define the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define the decision variables
x_vars = [pulp.LpVariable(f'x{i}', lowBound=None, upBound=None, cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective function: Maximize r
problem += r, "Objective"

# Adding constraints
for i in range(M):
    # Calculate the L2 norm of the row A[i]
    A_i_norm = np.linalg.norm(A[i, :])
    # Constraint: A.x + r * ||A_i||_2 <= b_i
    problem += (pulp.lpSum([A[i][j] * x_vars[j] for j in range(N)]) + r * A_i_norm <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')