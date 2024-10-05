import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Number of streets (N) and avenues (W)
N = len(data['north_time']) + 1
W = len(data['west_time'][0]) + 1

# Decision variables: x[n][w] and y[n][w]
x = [[pulp.LpVariable(f'x_{n}_{w}', cat='Binary') for w in range(W)] for n in range(N)]
y = [[pulp.LpVariable(f'y_{n}_{w}', cat='Binary') for w in range(W)] for n in range(N)]

# Problem definition
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum([data['west_time'][n][w] * x[n][w] for n in range(N) for w in range(W-1)]) + \
           pulp.lpSum([data['north_time'][n][w] * y[n][w] for n in range(N-1) for w in range(W)])

# Constraints
# Start at (0, 0)
problem += (x[0][0] + y[0][0] == 1)

# End at (N-1, W-1)
problem += (x[N-1][W-2] + y[N-2][W-1] == 1)

# Flow conservation
for n in range(N):
    for w in range(W):
        if n < N-1 and w < W-1:
            problem += (x[n][w] + y[n][w] == x[n][w+1] + y[n+1][w])
        elif n < N-1:
            problem += (y[n][w] == y[n+1][w])
        elif w < W-1:
            problem += (x[n][w] == x[n][w+1])

# Solve the problem
problem.solve()

# Extracting the solution
paths = []
current_n, current_w = 0, 0

while current_n < N-1 or current_w < W-1:
    if x[current_n][current_w].varValue == 1:
        current_w += 1
    else:
        current_n += 1
    paths.append((current_n, current_w))

total_time = pulp.value(problem.objective)

# Output result
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')