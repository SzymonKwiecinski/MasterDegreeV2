import pulp

# Parse input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Initialize LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables
y = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Set the objective to maximize the radius r
problem += r, "Maximize radius"

# Constraints
for i in range(M):
    lhs = pulp.lpSum(A[i][j] * y[j] for j in range(N))
    lhs += r * pulp.lpSum(A[i][j]**2 for j in range(N))**0.5
    problem += (lhs <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output the result
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')