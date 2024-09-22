import pulp
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = data['A']
b = data['B']

# Create the LP problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define variables for the center of the ball and the radius
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', cat='Continuous')

# Objective function: maximize the radius r
problem += r, "Objective"

# Constraints to ensure the ball is within the polytope
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= b[i] - r), f"Constraint_{i}"

# Solve the linear programming problem
problem.solve()

# Retrieve the center and radius
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Prepare output
output = {
    "center": center,
    "radius": radius
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')