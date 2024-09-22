import pulp
import numpy as np
import json

data = """{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}"""  # Changed single quotes to double quotes
data = json.loads(data)

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the problem
problem = pulp.LpProblem("ChebyshevCenter", pulp.LpMaximize)

# Decision variables
r = pulp.LpVariable('r', lowBound=0)  # radius
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]  # center coordinates

# Objective function to maximize r
problem += r

# Constraints
for i in range(M):
    a_i = A[i]
    problem += (np.dot(a_i, y) - r * np.linalg.norm(a_i) <= B[i])

# Solve the problem
problem.solve()

# Output the results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

output = {
    "center": center,
    "radius": radius
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')  # No changes needed here