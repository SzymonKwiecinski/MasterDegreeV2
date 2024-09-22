import pulp
import json

# Data input
data = json.loads("{'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}")

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the problem
problem = pulp.LpProblem("Chebyshev_Center_Problem", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)  # Center of the ball
r = pulp.LpVariable("r", lowBound=0)  # Radius of the ball

# Objective function: Maximize radius r
problem += r

# Constraints: Ensure the ball is within the defined set P
for i in range(M):
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= B[i] - r

for i in range(M):
    problem += pulp.lpSum(-A[i][j] * y[j] for j in range(N)) <= -B[i] + r

# Solve the problem
problem.solve()

# Extracting results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output result
output = {
    "center": center,
    "radius": radius
}

print(f'Output: {output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')