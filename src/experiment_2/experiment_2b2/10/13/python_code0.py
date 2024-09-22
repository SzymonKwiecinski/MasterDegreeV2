import pulp
import math
import json

# Parse input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the problem
problem = pulp.LpProblem("Maximize_Chebychev_Ball_Radius", pulp.LpMaximize)

# Define variables
y = [pulp.LpVariable(f'y_{j}', lowBound=None, upBound=None, cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Add constraints
for i in range(M):
    problem += (pulp.lpSum([A[i][j] * y[j] for j in range(N)]) + r * math.sqrt(pulp.lpSum([A[i][j] ** 2 for j in range(N)])) <= B[i]), f"Constraint_{i+1}"

# Objective function
problem += r

# Solve the problem
problem.solve()

# Prepare output
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Print results in specified format
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')