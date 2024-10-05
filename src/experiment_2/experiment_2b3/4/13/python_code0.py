import pulp
import json
import math

# Parse data
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')
M = data["M"]
N = data["N"]
A = data["A"]
B = data["B"]

# Initialize the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define variables for the center of the ball and the radius
y = [pulp.LpVariable(f'y_{j}', lowBound=None, cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective: maximize the radius
problem += r, "Objective"

# Constraints:
for i in range(M):
    constraint_expr = pulp.lpSum([A[i][j] * y[j] for j in range(N)]) + r * math.sqrt(sum(A[i][j] ** 2 for j in range(N)))
    problem += constraint_expr <= B[i], f'Constraint_{i}'

# Solve the problem
problem.solve()

# Prepare the output
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

output = {
    "center": center,
    "radius": radius
}

# Print the output and objective value
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')