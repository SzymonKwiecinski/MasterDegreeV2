import pulp
import json

# Input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the LP problem
problem = pulp.LpProblem("Chebyshev_Center_Problem", pulp.LpMaximize)

# Variables for the center of the ball
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]

# Variable for the radius of the ball
r = pulp.LpVariable("r", lowBound=0)

# Objective function: maximize the radius r
problem += r

# Constraints to ensure that the ball is within the feasible region
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= B[i] - r)

# Solve the problem
problem.solve()

# Extract the center and radius
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output the result
result = {
    "center": center,
    "radius": radius
}

# Print the objective value as requested
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')