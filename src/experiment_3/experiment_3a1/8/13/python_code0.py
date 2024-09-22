import pulp
import numpy as np
import json

# Data input
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective function: Maximize r
problem += r

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * np.linalg.norm(A[i]) <= B[i])

# Solve the problem
problem.solve()

# Output the results
center = [y[j].varValue for j in range(N)]
radius = r.varValue

output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')