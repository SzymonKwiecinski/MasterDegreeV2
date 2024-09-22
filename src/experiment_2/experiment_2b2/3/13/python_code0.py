import pulp

# Extracting data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables: x (center coordinates) and r (radius of the ball)
x_vars = [pulp.LpVariable(f"x_{i}", cat='Continuous') for i in range(N)]
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective function: Maximize the radius of the ball
problem += r, "Objective: Maximize r"

# Constraints: Ensure the ball with radius r is inside the polytope
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * x_vars[j] for j in range(N)) + r * pulp.lpSum(A[i][j]**2 for j in range(N))**0.5 <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(var) for var in x_vars]
radius = pulp.value(r)

# Output the results
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')