import pulp
import json

# Input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Extracting matrix A and vector b
A = data['A']
b = data['B']
M = data['M']
N = data['N']

# Define the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define variables for center of the ball
center = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
radius = pulp.LpVariable('r', lowBound=0)

# Define the objective function (maximize the radius)
problem += radius

# Add constraints for each linear inequality
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * center[j] for j in range(N)) <= b[i] - radius)

for i in range(M):
    problem += (pulp.lpSum(-A[i][j] * center[j] for j in range(N)) <= -b[i] + radius)

# Solve the problem
problem.solve()

# Collect results
center_values = [pulp.value(center[j]) for j in range(N)]
radius_value = pulp.value(radius)

# Output the result
output = {
    "center": center_values,
    "radius": radius_value
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')