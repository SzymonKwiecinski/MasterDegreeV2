import pulp

# Parse the data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

west_time = data["west_time"]
north_time = data["north_time"]

N = len(west_time)  # Number of streets (n)
W = len(west_time[0]) + 1  # Number of avenues (w)

# Define the problem
problem = pulp.LpProblem("Delivery_Path", pulp.LpMinimize)

# Decision variables
move_north = pulp.LpVariable.dicts("MoveNorth", ((n, w) for n in range(N-1) for w in range(W)), cat='Binary')
move_west = pulp.LpVariable.dicts("MoveWest", ((n, w) for n in range(N) for w in range(W-1)), cat='Binary')

# Objective function
problem += pulp.lpSum(north_time[n][w] * move_north[(n, w)] for n in range(N-1) for w in range(W)) + \
           pulp.lpSum(west_time[n][w] * move_west[(n, w)] for n in range(N) for w in range(W-1))

# Constraints
problem += move_west[(0, 0)] == 1, "Start_At_11"
for n in range(N):
    for w in range(W):
        # Flow conservation for north movement
        if n < N-1 and w < W:
            problem += move_north[(n, w)] <= 1  # There can only be one north movement per position
        if n < N and w < W-1:
            problem += move_west[(n, w)] <= 1  # There can only be one west movement per position

for n in range(N):
    for w in range(W):
        if n > 0 and w < W:  # Valid index for north movement
            problem += move_north[(n-1, w)] <= 1  # Ensuring we do not exceed dimensions

        if w > 0 and n < N:  # Valid index for west movement
            problem += move_west[(n, w-1)] <= 1  # Ensuring we do not exceed dimensions

# End conditions
problem += pulp.lpSum(move_north[(N-2, w)] for w in range(W)) + \
           pulp.lpSum(move_west[(n, W-2)] for n in range(N)) == 1, "End_At_WN"

# Solve the problem
problem.solve()

# Extract the path and total time
path = []
for n in range(N-1):
    for w in range(W):
        if pulp.value(move_north[(n, w)]) == 1:
            path.append((n+1, w+1))

for n in range(N):
    for w in range(W-1):
        if pulp.value(move_west[(n, w)]) == 1:
            path.append((n+1, w+1))

total_time = pulp.value(problem.objective)
output = {
    "paths": path,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')