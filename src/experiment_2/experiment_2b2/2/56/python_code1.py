import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract grid dimensions
N = len(data['north_time']) + 1
W = len(data['west_time'][0]) + 1

# Create the problem
problem = pulp.LpProblem("Minimize_Delivery_Time", pulp.LpMinimize)

# Create a dictionary of variables for north and west paths
north_vars = pulp.LpVariable.dicts("North", [(n, w) for n in range(N-1) for w in range(W)], cat='Binary')
west_vars = pulp.LpVariable.dicts("West", [(n, w) for n in range(N) for w in range(W-1)], cat='Binary')

# Objective function
problem += pulp.lpSum([north_vars[n, w] * data['north_time'][n][w] for n in range(N-1) for w in range(W)] +
                      [west_vars[n, w] * data['west_time'][n][w] for n in range(N) for w in range(W-1)])

# Constraints
# Start and end constraints
problem += (pulp.lpSum([north_vars[0, w] for w in range(W)] +
                       [west_vars[n, 0] for n in range(N)]) == 1, "Start_Path")

problem += (pulp.lpSum([north_vars[N-2, w] for w in range(W)] +
                       [west_vars[n, W-2] for n in range(N)]) == 1, "End_Path")

# Flow conservation constraints
for n in range(N):
    for w in range(W):
        inflow = 0
        outflow = 0
        if n < N-1:
            outflow += north_vars[n, w]
        if w < W-1:
            outflow += west_vars[n, w]
        if n > 0:
            inflow += north_vars[n-1, w]
        if w > 0:
            inflow += west_vars[n, w-1]
        if n < N-1 or w < W-1:
            problem += (inflow == outflow, f"Flow_Con_{n}_{w}")

# Solve the problem
problem.solve()

# Retrieve the optimal path and total time
paths = []
for n in range(N-1):
    for w in range(W):
        if north_vars[n, w].varValue == 1:
            paths.append((n+1, w+1, 'North'))

for n in range(N):
    for w in range(W-1):
        if west_vars[n, w].varValue == 1:
            paths.append((n+1, w+1, 'West'))

total_time = pulp.value(problem.objective)

# Output format
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')