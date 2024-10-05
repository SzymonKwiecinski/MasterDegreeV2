import pulp

# Input data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1
W = len(west_time[0]) + 1
m = N + W - 2

# Create the linear programming problem
problem = pulp.LpProblem("Shortest_Path_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w, 'north') for n in range(1, N) for w in range(1, W)),
                          cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, w, 'west') for n in range(1, N + 1) for w in range(1, W)),
                          cat='Binary')

# Objective function
problem += pulp.lpSum(
    north_time[n-1][w-1] * x[(n, w, 'north')] +
    west_time[n-1][w-1] * y[(n, w, 'west')]
    for n in range(1, N) for w in range(1, W)
)

# Constraints
# Flow constraints ensuring path through the network
for n in range(1, N+1):
    for w in range(1, W+1):
        if n == 1 and w == 1:
            continue
        if n == N and w == W:
            continue
        
        inflow = (x[(n-1, w, 'north')] if n > 1 else 0) + (y[(n, w-1, 'west')] if w > 1 else 0)
        outflow = (x[(n, w, 'north')] if n < N else 0) + (y[(n, w, 'west')] if w < W else 0)
        
        if n == 1:
            problem += outflow == 1
        elif w == 1:
            problem += outflow == 1
        elif n == N:
            problem += inflow == 1
        elif w == W:
            problem += inflow == 1
        else:
            problem += inflow == outflow

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Extract the path and total time
paths = []
for n in range(1, N):
    for w in range(1, W):
        if pulp.value(x[(n, w, 'north')]) == 1:
            paths.append((n+1, w))
        if pulp.value(y[(n, w, 'west')]) == 1:
            paths.append((n, w+1))

total_time = pulp.value(problem.objective)

# Output the results
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')