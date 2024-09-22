import pulp

# Data from JSON
west_time = [[3.5, 4.5], [4, 4], [5, 4]]
north_time = [[10, 10, 9], [9, 9, 12]]

N = len(north_time) + 1
W = len(west_time[0]) + 1

# Initialize the problem
problem = pulp.LpProblem("Optimal_Path_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', 
                          ((n, w) for n in range(N) for w in range(W)), 
                          0, 
                          1, 
                          pulp.LpBinary)

# Objective function
problem += pulp.lpSum(
    (north_time[n][w] * x[n, w] if n < N-1 and w < W-1 else 0) + 
    (west_time[n][w] * x[n, w] if n < N-1 and w < W-1 else 0)
    for n in range(N-1) for w in range(W-1)
)

# Constraints
for n in range(N-1):
    for w in range(W-1):
        if n != N-1 and w != W-1:
            problem += x[n, w] + x[n, w+1] - x[n+1, w] == 0  # Flow conservation simplified

# Starting point
problem += pulp.lpSum(x[0, w] for w in range(W-1)) == 1

# Ending point
problem += pulp.lpSum(x[n, W-2] for n in range(N-1)) == 1

# Solve
problem.solve()

# Print Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Extract the optimal path
paths = []
current_n, current_w = 0, 0

while current_n < N-1 or current_w < W-1:
    if current_w < W-1 and pulp.value(x[current_n, current_w]) == 1:
        current_w += 1
    elif current_n < N-1 and pulp.value(x[current_n, current_w]) == 1:
        current_n += 1
    paths.append((current_n, current_w))

# Output the path and total time
print("Optimal Path (intersections):", paths)
print("Total travel time:", pulp.value(problem.objective))