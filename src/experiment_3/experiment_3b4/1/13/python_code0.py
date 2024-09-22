import pulp
import numpy as np

# Problem data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = data['B']

# Create a linear programming problem
problem = pulp.LpProblem("MaximizeBallRadius", pulp.LpMaximize)

# Decision variables
y = [pulp.LpVariable(f'y{i}', cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective function: Maximize r
problem += r

# Constraints
for i in range(M):
    norm_ai = np.linalg.norm(A[i])
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) + norm_ai * r <= B[i]

# Solve the problem
problem.solve()

# Display the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')