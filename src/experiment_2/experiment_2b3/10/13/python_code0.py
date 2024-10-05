import pulp

# Define the data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M, N, A, B = data['M'], data['N'], data['A'], data['B']

# Define the LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define variables: center y and radius r
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective function: Maximize the radius r
problem += r, "Maximize_Radius"

# Constraints: each inequality defines part of the set P
for i in range(M):
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * (sum(A[i][j]**2 for j in range(N))**0.5) <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(var) for var in y]
radius = pulp.value(r)

# Output in the requested format
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')