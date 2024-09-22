import pulp
import json

# Given data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Number of constraints (m) and number of variables (n)
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define variables: the center of the ball (y) and the radius (r)
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Set objective: maximize the radius
problem += r

# Add constraints for the ball to be within the set P
for i in range(M):
    constraint = pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= B[i] - r
    problem += constraint
    constraint = pulp.lpSum(A[i][j] * y[j] for j in range(N)) >= B[i] - r
    problem += constraint

# Solve the problem
problem.solve()

# Retrieve results
center = [pulp.value(y_j) for y_j in y]
radius = pulp.value(r)

# Output the results
result = {
    "center": center,
    "radius": radius
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')