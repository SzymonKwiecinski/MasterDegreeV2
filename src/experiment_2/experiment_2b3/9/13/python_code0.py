import pulp
import json
import numpy as np

# Load the data
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')

# Extract values
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create a LP problem
problem = pulp.LpProblem("ChebyshevCenter", pulp.LpMaximize)

# Create decision variables
y = [pulp.LpVariable(f'y_{j}', lowBound=None, upBound=None, cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective: Maximize the radius of the ball
problem += r

# Add constraints
for i in range(M):
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) + np.linalg.norm(A[i]) * r <= B[i]

# Solve the problem
problem.solve()

# Extract solution
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Prepare the output
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')