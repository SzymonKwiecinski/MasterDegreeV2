import pulp
import json

# Input data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Radius", pulp.LpMaximize)

# Variables for the center of the ball
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)

# Variable for the radius
r = pulp.LpVariable("r", lowBound=0)

# Objective function: maximize the radius
problem += r, "Objective"

# Constraints
for i in range(M):
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= B[i] - r, f"Constraint_{i+1}"

for i in range(M):
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) >= B[i] - r, f"Constraint_{i+1}_lower"

# Solve the problem
problem.solve()

# Output the center and radius
center = [y[j].varValue for j in range(N)]
radius = r.varValue

output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')