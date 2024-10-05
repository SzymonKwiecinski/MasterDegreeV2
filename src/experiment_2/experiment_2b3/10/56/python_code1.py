import pulp

# Input data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

west_time = data['west_time']
north_time = data['north_time']

# Determine dimensions
N = len(north_time) + 1  # Number of streets (rows)
W = len(west_time[0]) + 1 # Number of avenues (columns)

# Create the linear programming problem
problem = pulp.LpProblem("Shortest_Path_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum(
    north_time[n-1][w-1] * x[(n, w)] +
    west_time[n-1][w-1] * y[(n, w)]
    for n in range(1, N) for w in range(1, W)
)

# Constraints
# Flow constraints ensuring path through the network
for n in range(1, N):
    for w in range(1, W):
        inflow = (x[(n - 1, w)] if n > 1 else 0) + (y[(n, w - 1)] if w > 1 else 0)
        outflow = (x[(n, w)] if n < N - 1 else 0) + (y[(n, w)] if w < W - 1 else 0)
        
        if n == 1 and w == 1:
            problem += outflow == 1  # Starting point
        elif n == N - 1 and w == W - 1:
            problem += inflow == 1  # End point
        else:
            problem += inflow == outflow  # Flow conservation

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Extract the path and total time
paths = []
for n in range(1, N):
    for w in range(1, W):
        if pulp.value(x[(n, w)]) == 1:
            paths.append((n + 1, w))  # Moving north
        if pulp.value(y[(n, w)]) == 1:
            paths.append((n, w + 1))  # Moving west

total_time = pulp.value(problem.objective)

# Output the results
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f'(Objective Value): <OBJ>{total_time}</OBJ>')