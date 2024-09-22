import pulp
import json

# Input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Set up the problem
N = data['N']
M = data['M']
A = data['A']
b = data['B']

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables for the center of the ball
y = [pulp.LpVariable(f'y_{j}', None, None) for j in range(N)]
# Decision variable for the radius of the ball
r = pulp.LpVariable('r', lowBound=0)

# Objective function: maximize the radius of the ball
problem += r

# Adding constraints to the problem
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= b[i] - r)
    problem += (pulp.lpSum(-A[i][j] * y[j] for j in range(N)) <= -b[i] + r)

# Solve the problem
problem.solve()

# Prepare output
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Print objective value and output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
output = {
    "center": center,
    "radius": radius
}
print(output)