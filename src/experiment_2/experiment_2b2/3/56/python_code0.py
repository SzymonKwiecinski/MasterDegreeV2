import pulp

# Data from the input
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

west_time = data['west_time']
north_time = data['north_time']

N = len(west_time)  # Number of rows
W = len(west_time[0]) + 1  # Number of columns

# Create the LP problem
problem = pulp.LpProblem("Optimal_Delivery_Path", pulp.LpMinimize)

# Decision variables: whether the path uses each segment
x_west = [[pulp.LpVariable(f'x_w_{n}_{w}', cat='Binary') for w in range(0, W-1)] for n in range(N)]
x_north = [[pulp.LpVariable(f'x_n_{n}_{w}', cat='Binary') for w in range(W)] for n in range(N-1)]

# Objective function: Minimize the total travel time
problem += pulp.lpSum(west_time[n][w] * x_west[n][w] for n in range(N) for w in range(W-1)) + \
           pulp.lpSum(north_time[n][w] * x_north[n][w] for n in range(N-1) for w in range(W))

# Adding constraints for the flow of path
# Start at (1,1) and end at (N,W)
problem += x_north[0][0] == 1  # Start point constraint

for n in range(N):
    for w in range(W):
        if n < N-1 and w < W-1:
            # Flow balance constraints for nodes not at the edge
            problem += x_north[n][w] + x_west[n][w] == x_west[n][w-1] + x_north[n-1][w]
        elif n < N-1:
            # Edge case for the last column
            problem += x_north[n][w] == x_north[n-1][w] + x_west[n-1][w]
        elif w < W-1:
            # Edge case for the last row
            problem += x_west[n][w] == x_west[n][w-1] + x_north[n-1][w]
        else:
            # End point constraint
            problem += x_west[n][w-1] == 1

# Solve the problem
problem.solve()

# Extracting the solution
path = []
for n in range(N):
    for w in range(W-1):
        if pulp.value(x_west[n][w]) == 1:
            path.append((n+1, w+1))  # Convert to 1-indexed

for n in range(N-1):
    for w in range(W):
        if pulp.value(x_north[n][w]) == 1:
            path.append((n+1, w+1))  # Convert to 1-indexed

# Calculate the total travel time
total_travel_time = pulp.value(problem.objective)

# Output format
output = {
    "paths": path,
    "total_time": total_travel_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')