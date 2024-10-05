import pulp

# Parse the given data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create a linear programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')  # radius r must be non-negative

# Objective function: Maximize the radius r
problem += r

# Constraints: Each inequality defines an inward-pointing half-space
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * (sum(A[i][j]**2 for j in range(N))**0.5) <= B[i])

# Solve the problem
problem.solve()

# Get the results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Print the results in the specified output format
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')