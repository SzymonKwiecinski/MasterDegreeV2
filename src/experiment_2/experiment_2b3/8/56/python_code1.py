import pulp

# Read the data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract the west_time and north_time matrices
west_time = data["west_time"]
north_time = data["north_time"]

# Dimensions of the grid
N = len(north_time) + 1
W = len(west_time[0]) + 1

# Create the LP problem
problem = pulp.LpProblem("Optimal_Path", pulp.LpMinimize)

# Decision variables for moving west and north
x_west = pulp.LpVariable.dicts("x_west", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
x_north = pulp.LpVariable.dicts("x_north", ((n, w) for n in range(1, N) for w in range(1, W + 1)), cat='Binary')

# Objective function: Minimize the total travel time
problem += (
    pulp.lpSum(west_time[n-1][w-1] * x_west[n, w] for n in range(1, N) for w in range(1, W)) +
    pulp.lpSum(north_time[n-1][w-1] * x_north[n, w] for n in range(1, N) for w in range(1, W + 1))
)

# Initial condition
problem += x_west[1, 1] == 1

# Final condition
problem += x_west[N-1, W-1] + x_north[N-1, W] == 1

# Flow conservation constraints
for n in range(1, N):
    for w in range(1, W):
        # Ensure not to exceed boundaries
        if w < W - 1:
            problem += x_west[n, w] + x_north[n, w] == x_west[n, w + 1] + x_north[n + 1, w]

# Solve the problem
problem.solve()

# Extract the path and total time
paths = [(n, w) for n in range(1, N) for w in range(1, W) if x_west[n, w].varValue == 1]
total_time = pulp.value(problem.objective)

# Output the result
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')