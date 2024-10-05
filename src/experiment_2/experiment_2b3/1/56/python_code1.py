import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Number of streets (N) and avenues (W)
N = len(data['north_time']) + 1
W = len(data['west_time'][0]) + 1

# Decision variables: x[n][w] for west moves, y[n][w] for north moves
x = [[pulp.LpVariable(f'x_{n}_{w}', cat='Binary') for w in range(W-1)] for n in range(N)]
y = [[pulp.LpVariable(f'y_{n}_{w}', cat='Binary') for w in range(W)] for n in range(N-1)]

# Problem definition
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum([data['west_time'][n][w] * x[n][w] for n in range(N) for w in range(W-1)]) + \
           pulp.lpSum([data['north_time'][n][w] * y[n][w] for n in range(N-1) for w in range(W)])

# Constraints
# Start at (0, 0)
problem += (pulp.lpSum([x[0][w] for w in range(W-1)]) + pulp.lpSum([y[0][w] for w in range(W)]) == 1)

# End at (N-1, W-1)
problem += (pulp.lpSum([x[N-1][w] for w in range(W-1)]) + pulp.lpSum([y[N-2][w] for w in range(W)]) == 1)

# Flow conservation
for n in range(N):
    for w in range(W):
        if n < N-1 and w < W-1:
            problem += (pulp.lpSum([x[n][w] for w in range(W-1)]) + pulp.lpSum([y[n][w] for w in range(W)]) -
                         pulp.lpSum([x[n][w+1] for w in range(W-2)]) - 
                         pulp.lpSum([y[n+1][w] for w in range(W)]) == 0)

# Solve the problem
problem.solve()

# Extracting the solution
paths = []
total_time = pulp.value(problem.objective)

# Backtracking to find the path taken
current_n, current_w = 0, 0
while current_n < N-1 or current_w < W-1:
    if current_w < W-1 and x[current_n][current_w].varValue == 1:
        paths.append((current_n, current_w))
        current_w += 1
    elif current_n < N-1 and y[current_n][current_w].varValue == 1:
        paths.append((current_n, current_w))
        current_n += 1

# Add the last intersection
paths.append((N-1, W-1))

# Output result
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')