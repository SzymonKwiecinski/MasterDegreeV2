import pulp
import json

# Input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Extracting the number of constraints and dimensions
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables for the center of the ball
y = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
# Variable for the radius
r = pulp.LpVariable('r', lowBound=0)

# Objective function: Maximize r
problem += r

# Constraints: a_i^T * y <= b_i - r and -a_i^T * y <= -b_i - r
for i in range(M):
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= B[i] - r
    problem += pulp.lpSum(-A[i][j] * y[j] for j in range(N)) <= -B[i] - r

# Solve the problem
problem.solve()

# Prepare the output
center = [y[j].varValue for j in range(N)]
radius = r.varValue

# JSON output format
output = {
    "center": center,
    "radius": radius
}

# Print the objective value and output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(output))