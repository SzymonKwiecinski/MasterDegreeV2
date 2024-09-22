import pulp

# Data from the JSON format
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

west_time = data['west_time']
north_time = data['north_time']

# Sizes of the grid
N = len(north_time) + 1
W = len(west_time[0]) + 1

# Create a LP problem
problem = pulp.LpProblem("Shortest_Path_Problem", pulp.LpMinimize)

# Decision variables
west_vars = pulp.LpVariable.dicts("West", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
north_vars = pulp.LpVariable.dicts("North", ((n, w) for n in range(1, N) for w in range(1, W + 1)), cat='Binary')

# Objective function: Minimize total travel time
problem += (pulp.lpSum(west_time[n-1][w-1] * west_vars[(n, w)] for n in range(1, N) for w in range(1, W)) +
            pulp.lpSum(north_time[n-1][w-1] * north_vars[(n, w)] for n in range(1, N) for w in range(1, W + 1))), "Total_Travel_Time"

# Constraints

# Flow constraints
for n in range(1, N):
    for w in range(1, W):
        if n == 1 and w == 1:
            problem += north_vars[(n, w)] + west_vars[(n, w)] == 1, f"Start_at_{n}_{w}"
        else:
            inflow = (north_vars[(n - 1, w)] if n > 1 else 0) + (west_vars[(n, w - 1)] if w > 1 else 0)
            outflow = north_vars[(n, w)] + west_vars[(n, w)]
            problem += inflow - outflow == 0, f"Flow_conservation_at_{n}_{w}"

# Only one outgoing path from each node except the endpoint
problem += west_vars[(N-1, W-1)] + north_vars[(N-1, W)] == 1, "Reach_End"

# Solve the problem
problem.solve()

# Compile the solution
paths = []
n, w = 1, 1
visited = set()
while (n, w) not in visited:
    visited.add((n, w))
    
    if n < N and north_vars[(n, w)].varValue == 1:
        paths.append((n, w))
        n += 1
    elif w < W and west_vars[(n, w)].varValue == 1:
        paths.append((n, w))
        w += 1
    else:
        break

total_time = pulp.value(problem.objective)

# Output the results
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')