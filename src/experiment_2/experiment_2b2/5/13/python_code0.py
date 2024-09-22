import pulp

# Define the data
data = {
    "M": 4,
    "N": 2,
    "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    "B": [2.0, 2.0, 3.0, 5.0]
}

# Extract data
M = data["M"]
N = data["N"]
A = data["A"]
B = data["B"]

# Define the LP problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define variables: center coordinates y_j and radius r
y = [pulp.LpVariable(f"y_{j}", lowBound=None, upBound=None, cat='Continuous') for j in range(N)]
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective: Maximize radius r
problem += r, "Objective: Maximize radius"

# Constraints: Ensure the ball is within the polytope
for i in range(M):
    problem += pulp.lpSum([A[i][j] * y[j] for j in range(N)]) + r * (sum(A[i][j]**2 for j in range(N))**0.5) <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(y_j) for y_j in y]
radius = pulp.value(r)

# Print the results in the specified format
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')