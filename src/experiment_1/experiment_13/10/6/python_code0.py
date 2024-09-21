import pulp
import numpy as np

# Data from JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variable
r = pulp.LpVariable("r", lowBound=0)  # r >= 0

# Constraints
x = [pulp.LpVariable(f'x_{i}', cat='Continuous') for i in range(N)]

for i in range(M):
    problem += (pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * np.linalg.norm(A[i]) <= B[i], f"constraint_{i+1}")

# Objective function
problem += r  # Maximize r

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')