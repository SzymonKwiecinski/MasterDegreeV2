import pulp
import json

# Input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
A = data['A']
b = data['B']
N = data['N']

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables for the center of the ball
y = [pulp.LpVariable(f'y_{i}', cat='Continuous') for i in range(N)]
# Decision variable for the radius
r = pulp.LpVariable("r", lowBound=0)

# Objective function: Maximize the radius
problem += r

# Constraints for the linear inequalities
for i in range(len(A)):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= b[i] - r)

for i in range(len(A)):
    problem += (pulp.lpSum(-A[i][j] * y[j] for j in range(N)) <= -b[i] + r)

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(y[i]) for i in range(N)]
radius = pulp.value(r)

# Output the results
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')