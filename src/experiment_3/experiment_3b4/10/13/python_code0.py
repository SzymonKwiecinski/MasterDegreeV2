import pulp
import numpy as np

# Data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the problem
problem = pulp.LpProblem("Largest_Inscribed_Ball", pulp.LpMaximize)

# Define variables
y = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective function
problem += r, "Maximize_Radius"

# Constraints
for i in range(M):
    a_i = np.array(A[i])
    norm_a_i = np.linalg.norm(a_i)
    problem += (pulp.lpSum(a_i[j] * y[j] for j in range(N)) + r * norm_a_i <= B[i]), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')