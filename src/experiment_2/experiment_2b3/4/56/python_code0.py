import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1
W = len(west_time[0]) + 1

# Initialize LP problem
problem = pulp.LpProblem("Delivery_Time_Minimization", pulp.LpMinimize)

# Decision variables
move_west = pulp.LpVariable.dicts("Move_West", (range(N), range(W - 1)), 0, 1, pulp.LpBinary)
move_north = pulp.LpVariable.dicts("Move_North", (range(N - 1), range(W)), 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum([
    west_time[n][w] * move_west[n][w] for n in range(N) for w in range(W - 1)
]) + pulp.lpSum([
    north_time[n][w] * move_north[n][w] for n in range(N - 1) for w in range(W)
])

# Constraints

# Start at (0, 0)
problem += move_west[0][0] + move_north[0][0] == 1

# Ensuring path continuity
for n in range(N):
    for w in range(W):
        if n > 0:
            problem += move_north[n - 1][w] + (move_west[n][w - 1] if w > 0 else 0) >= (move_west[n][w] if w < W - 1 else 0) + (move_north[n][w] if n < N - 1 else 0)

for n in range(N):
    # Can't go north from last row
    if n == N - 1:
        for w in range(W):
            problem += move_north[n - 1][w] == (move_west[n][w] if w < W - 1 else 0)
            
    # Can't go west from last column
    if n < N - 1:
        problem += move_west[n][W - 2] == move_north[n][W - 1]

# Solve the problem
problem.solve()

# Extract results
paths = []
for n in range(N):
    for w in range(W):
        if w < W - 1 and pulp.value(move_west[n][w]) == 1:
            paths.append((n+1, w+2))  # Order of stepping
        if n < N - 1 and pulp.value(move_north[n][w]) == 1:
            paths.append((n+2, w+1))

total_time = pulp.value(problem.objective)

# Output result
output = {
    "paths": paths,
    "total_time": total_time
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')