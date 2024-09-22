import pulp
import json
import numpy as np

# Parse the input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
A = np.array(data["A"])
b = np.array(data["B"])
m, n = data["M"], data["N"]

# Create a linear programming problem
problem = pulp.LpProblem("ChebyshevCenter", pulp.LpMaximize)

# Define variables for the center of the ball (y = [y1, y2, ...]) and the radius (r)
y = pulp.LpVariable.dicts("y", range(n), lowBound=None, upBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective function: Maximize the radius r
problem += r, "Maximize_Radius"

# Constraints: a_i^T * y + r * ||a_i|| <= b_i
for i in range(m):
    norm_ai = np.linalg.norm(A[i])
    problem += pulp.lpSum([A[i][j] * y[j] for j in range(n)]) + r * norm_ai <= b[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(y[j]) for j in range(n)]
radius = pulp.value(r)

# Prepare output
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output, indent=4))
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")