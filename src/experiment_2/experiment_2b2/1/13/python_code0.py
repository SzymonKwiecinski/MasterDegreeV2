import pulp
import math

# Parse the input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Initialize the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables for the center of the ball in R^N
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]

# Variable for the radius of the ball
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective: Maximize the radius r
problem += r, "Maximize_radius"

# Constraints: A_i * y + r * ||A_i|| <= B_i for all i
for i in range(M):
    norm_ai = math.sqrt(sum(A[i][j] ** 2 for j in range(N)))  # Euclidean norm of A_i
    problem += pulp.lpDot(A[i], y) + r * norm_ai <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Retrieve the results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output the results
output = {"center": center, "radius": radius}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')