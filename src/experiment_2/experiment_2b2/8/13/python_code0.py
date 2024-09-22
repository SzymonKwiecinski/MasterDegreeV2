import pulp
import numpy as np

# Parse the data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Initialize the LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables: y (center of the ball) and r (radius of the ball)
y = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective function: Maximize the radius r
problem += r, "Objective"

# Adding constraints to the problem
for i in range(M):
    norm_ai = np.linalg.norm(A[i])  # Compute the Euclidean norm of a_i
    problem += (pulp.lpDot(A[i], y) + norm_ai * r <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract solutions
center = [y[j].varValue for j in range(N)]
radius = r.varValue

# Prepare the output in required format
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")