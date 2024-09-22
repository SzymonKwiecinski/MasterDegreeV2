import pulp
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Extract data
A = data['A']
b = data['B']
N = data['N']

# Create a LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables for the center of the ball and radius
y = [pulp.LpVariable(f'y_{i}', lowBound=None) for i in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# The objective is to maximize the radius r
problem += r

# Constraints to define the ball within the region P
for i in range(len(A)):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= b[i] - r)
    problem += (pulp.lpSum(-A[i][j] * y[j] for j in range(N)) <= b[i] - r)

# Solve the problem
problem.solve()

# Get the center and radius
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output the result in the specified format
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')