import pulp
import json

# Input data
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables
r = pulp.LpVariable("r", lowBound=0)  # Radius
y = [pulp.LpVariable(f"y_{j}", cat='Continuous') for j in range(N)]  # Center coordinates

# Objective function
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) - r <= B[i]), f"Constraint_upper_{i}"
    problem += (-pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r <= 0), f"Constraint_lower_{i}"

# Solve the problem
problem.solve()

# Output results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

print(f'Center of the ball: {center}')
print(f'Radius of the ball: {radius}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')