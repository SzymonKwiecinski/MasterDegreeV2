import pulp

# Parse the input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

# Grid dimensions
N = len(north_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Create the LP problem
problem = pulp.LpProblem("Minimize_Walking_Time", pulp.LpMinimize)

# Decision variables
xwest = pulp.LpVariable.dicts("xwest", ((n, w) for n in range(1, N+1) for w in range(1, W)), cat='Binary')
xnorth = pulp.LpVariable.dicts("xnorth", ((n, w) for n in range(1, N) for w in range(1, W+1)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * xwest[n, w] for n in range(1, N+1) for w in range(1, W) if w < W) +
    pulp.lpSum(north_time[n-1][w-1] * xnorth[n, w] for n in range(1, N) for w in range(1, W+1) if n < N)
), "Total Travel Time"

# Flow constraints
for n in range(1, N+1):
    for w in range(1, W+1):
        incoming_flow = (
            xwest[n, w-1] if w > 1 else 0
        ) + (
            xnorth[n-1, w] if n > 1 else 0
        )
        outgoing_flow = (
            xwest[n, w] if w < W else 0
        ) + (
            xnorth[n, w] if n < N else 0
        )
        if n == 1 and w == 1:
            problem += outgoing_flow == 1, f"Start at intersection ({n},{w})"
        elif n == N and w == W:
            problem += incoming_flow == 1, f"End at intersection ({n},{w})"
        else:
            problem += incoming_flow == outgoing_flow, f"Flow conservation at ({n},{w})"

# Solve the problem
problem.solve()

# Extract solution
paths = []
for n in range(1, N+1):
    for w in range(1, W):
        if pulp.value(xwest[n, w]) == 1:
            paths.append((n, w))
for n in range(1, N):
    for w in range(1, W+1):
        if pulp.value(xnorth[n, w]) == 1:
            paths.append((n, w))

total_time = pulp.value(problem.objective)

# Output format
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')