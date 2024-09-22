import pulp
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Extracting data
M = data['M']
N = data['N']
A = data['A']
b = data['B']

# Create a linear programming problem
problem = pulp.LpProblem("Largest_Ball_Within_P", pulp.LpMaximize)

# Variables: center of the ball (y) and radius (r)
y = [pulp.LpVariable(f'y_{i}', lowBound=None) for i in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective: Maximize radius
problem += r

# Constraints: Each constraint of the form a_i^T * y <= b_i + r
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= b[i] - r)

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Print the results in the specified format
output = {
    "center": center,
    "radius": radius
}

# Output the results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')