import pulp
import numpy as np
import json

# Data input
data = '''<DATA>
{'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}</DATA>'''
data_dict = json.loads(data.replace("<DATA>", "").replace("</DATA>", "").strip())

# Extract data
M = data_dict['M']
N = data_dict['N']
A = np.array(data_dict['A'])
B = np.array(data_dict['B'])

# Setup problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables: x (center of the ball) and r (radius of the ball)
x = [pulp.LpVariable(f'x_{i}', lowBound=None, cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective function: Maximize the radius
problem += r, "Maximize Radius"

# Constraints: Ax + ||a_i||r <= b
for i in range(M):
    norm_a_i = np.linalg.norm(A[i])
    problem += (pulp.lpSum(A[i][j] * x[j] for j in range(N)) + norm_a_i * r <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(x[i]) for i in range(N)]
radius = pulp.value(r)

# Output
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')