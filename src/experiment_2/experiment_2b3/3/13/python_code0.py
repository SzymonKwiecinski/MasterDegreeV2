import pulp
import math

# Parse the input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
A = data['A']
B = data['B']
M = data['M']
N = data['N']

# Create a Linear Programming problem
problem = pulp.LpProblem("ChebychevCenter", pulp.LpMaximize)

# Define the variables y (center of the ball) and r (radius of the ball)
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')  # Radius cannot be negative

# Objective function: Maximize the radius r
problem += r

# Constraints: Each constraint should maintain the ball within the polyhedron
for i in range(M):
    # Constraint: a_i^T * y + r * ||a_i|| <= b_i
    norm_a_i = math.sqrt(sum(aij * aij for aij in A[i]))  # Euclidean norm of a_i
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * norm_a_i <= B[i])

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(var) for var in y]
radius = pulp.value(r)

# Print the result in the specified format
output = {"center": center, "radius": radius}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')