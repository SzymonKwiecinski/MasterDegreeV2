import pulp
import numpy as np

# Define the data
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
problem = pulp.LpProblem("ChebychevCenter", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (i for i in range(N)), lowBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')  # Radius

# Objective function
problem += r, "Maximize Radius"

# Constraints
for i in range(M):
    # Calculate the Euclidean norm of the i-th row of A
    A_i_norm = np.linalg.norm(A[i])
    # Add the constraint: A_i x + r * ||A_i||_2 <= B_i
    problem += (pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * A_i_norm <= B[i]), f"Constraint {i+1}"

# Solve the problem
problem.solve()

# Print results
print(f'Status: {pulp.LpStatus[problem.status]}')
for j in range(N):
    print(f'x[{j}] = {pulp.value(x[j])}')
print(f'r = {pulp.value(r)} (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')