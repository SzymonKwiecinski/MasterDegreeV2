import pulp
import json

# Input data extraction
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
A = data['A']
b = data['B']
N = data['N']

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define variables: center of the ball (y) and radius (r)
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective function: maximize r
problem += r

# Constraints for the ball to be inside the feasible set P
for i in range(len(A)):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= b[i] - r)

# Solve the problem
problem.solve()

# Extract results
center = [y[j].varValue for j in range(N)]
radius = r.varValue

# Output formatting
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')