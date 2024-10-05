import pulp

# The given data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Unpack data
west_time = data['west_time']
north_time = data['north_time']

# Dimensions
N = len(north_time) + 1
W = len(west_time[0]) + 1

# Initialize the LP problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Decision variables
x_north = pulp.LpVariable.dicts("north", [(n, w) for n in range(N-1) for w in range(W)], cat='Binary')
x_west = pulp.LpVariable.dicts("west", [(n, w) for n in range(N) for w in range(W-1)], cat='Binary')

# Objective function: Minimize total travel time
total_time = (
    pulp.lpSum(north_time[n][w] * x_north[n, w] for n in range(N-1) for w in range(W)) +
    pulp.lpSum(west_time[n][w] * x_west[n, w] for n in range(N) for w in range(W-1))
)
problem += total_time

# Constraints

# Flow entering starting point (1,1)
problem += x_north[0, 0] + x_west[0, 0] == 1

# Flow conservation for each intersection (n, w)
for n in range(N):
    for w in range(W):
        if n == 0 and w == 0:
            continue  # Start point constraints already added
        inflow = 0
        outflow = 0
        
        if n > 0:
            inflow += x_north[n-1, w]
        if w > 0:
            inflow += x_west[n, w-1]
        
        if n < N-1:
            outflow += x_north[n, w]
        if w < W-1:
            outflow += x_west[n, w]
        
        problem += inflow == outflow

# Flow leaving destination point (N, W)
problem += x_north[N-2, W-1] + x_west[N-1, W-2] == 1

# Solve the problem
problem.solve()

# Extract the path
paths = []
for n in range(N-1):
    for w in range(W):
        if pulp.value(x_north[n, w]) == 1:
            paths.append((n+1, w+1))

for n in range(N):
    for w in range(W-1):
        if pulp.value(x_west[n, w]) == 1:
            paths.append((n+1, w+1))

# Collect results
result = {
    "paths": paths,
    "total_time": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')