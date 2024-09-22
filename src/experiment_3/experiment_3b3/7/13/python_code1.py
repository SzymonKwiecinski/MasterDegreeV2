import pulp

# Extract data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
A = data['A']
b = data['B']
m = data['M']
n = data['N']

# Create a LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables for the center of the ball and the radius
y = [pulp.LpVariable(f'y_{i}', cat='Continuous') for i in range(n)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')  # radius, non-negative

# Objective: maximize the radius
problem += r

# Constraints: ||Ax - b|| <= r
for i in range(m):
    constraint_expr = pulp.lpSum([A[i][j] * y[j] for j in range(n)]) + r
    problem += (constraint_expr <= b[i])

# Solve the problem
problem.solve()

# Output: center and radius
center = [pulp.value(y_var) for y_var in y]
radius = pulp.value(r)

print({
    "center": center,
    "radius": radius
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')