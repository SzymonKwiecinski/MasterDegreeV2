import pulp

# Parse input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data["west_time"]
north_time = data["north_time"]

# Variables for grid dimensions
N = len(west_time)
W = len(west_time[0]) + 1

# Initialize the LP problem
problem = pulp.LpProblem("Delivery_Path_Minimization", pulp.LpMinimize)

# Decision variables
x_vars = pulp.LpVariable.dicts("x", [(n, w) for n in range(N) for w in range(W-1)], lowBound=0, cat='Binary')
y_vars = pulp.LpVariable.dicts("y", [(n, w) for n in range(N-1) for w in range(W)], lowBound=0, cat='Binary')

# Objective function: Minimize the total travel time
problem += (
    pulp.lpSum(west_time[n][w] * x_vars[(n, w)] for n in range(N) for w in range(W-1)) +
    pulp.lpSum(north_time[n][w] * y_vars[(n, w)] for n in range(N-1) for w in range(W))
)

# Constraints
# Start at (0, 0)
problem += x_vars[(0, 0)] + y_vars[(0, 0)] == 1

# Flow conservation constraints
for n in range(N):
    for w in range(W):
        # At (n, w), if not on the right boundary, consider going west
        if w < W - 1:
            problem += x_vars[(n, w)] - (x_vars[(n, w+1)] if w+1 < W-1 else 0) - (y_vars[(n+1, w)] if n+1 < N else 0) <= 0
        # At (n, w), if not on the top boundary, consider going north
        if n < N - 1:
            problem += y_vars[(n, w)] - (y_vars[(n+1, w)] if n+1 < N-1 else 0) - (x_vars[(n, w+1)] if w < W-1 else 0) <= 0

# Solve the problem
problem.solve()

# Extract paths
paths = []
for n in range(N):
    for w in range(W-1):
        if x_vars[(n, w)].varValue > 0.5:
            paths.append((n+1, w+1))

for n in range(N-1):
    for w in range(W):
        if y_vars[(n, w)].varValue > 0.5:
            paths.append((n+1, w+1))

# Prepare output
output = {
    "paths": paths,
    "total_time": pulp.value(problem.objective)
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')