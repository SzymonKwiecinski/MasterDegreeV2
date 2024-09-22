import pulp
import numpy as np
import json

# Input data
data = '{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}'
data = json.loads(data)

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define the variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective function: maximize r
problem += r

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) - r * np.linalg.norm(A[i]) <= B[i])

# Solve the problem
problem.solve()

# Extract results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

print(f'Center: {center}')
print(f'Radius: {radius}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')