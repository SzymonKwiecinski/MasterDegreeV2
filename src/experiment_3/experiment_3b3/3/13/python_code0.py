import pulp
import numpy as np

# Data from JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Problem
problem = pulp.LpProblem("Maximize_Radius", pulp.LpMaximize)

# Variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Constraints
for i in range(M):
    problem += pulp.lpSum(A[i][j] * (y[j] + r) for j in range(N)) <= B[i]

# Objective
problem += r

# Solve the problem
problem.solve()

# Extracting results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output
result = {"center": center, "radius": radius}
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')