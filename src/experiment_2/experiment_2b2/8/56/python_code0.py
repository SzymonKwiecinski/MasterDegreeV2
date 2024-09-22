import pulp
import json

# Input data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Dimensions of the grid
N = len(data['north_time']) + 1
W = len(data['west_time'][0]) + 1

# Create the LP problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Decision variables
x_north = pulp.LpVariable.dicts("North", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
x_west = pulp.LpVariable.dicts("West", ((n, w) for n in range(1, N + 1) for w in range(1, W)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(data['north_time'][n-1][w-1] * x_north[n, w] for n in range(1, N) for w in range(1, W))
    + pulp.lpSum(data['west_time'][n-1][w-1] * x_west[n, w] for n in range(1, N + 1) for w in range(1, W))
)

# Constraints
for n in range(1, N):
    for w in range(1, W):
        # Flow balance at each interior intersection
        if n > 1 and w > 1:
            problem += (x_north[n-1, w] + x_west[n, w-1] == x_north[n, w] + x_west[n, w])

# Ensure that we start at the initial position
problem += x_west[1, 1] == 1

# Ensure that we reach the final position
problem += x_north[N-1, W-1] == 1

# Solve the problem
problem.solve()

# Output results
paths = []
total_time = pulp.value(problem.objective)

for n in range(1, N):
    for w in range(1, W):
        if pulp.value(x_north[n, w]) == 1:
            paths.append((n, w))
        if pulp.value(x_west[n, w]) == 1:
            paths.append((n, w))

output = {
    "paths": paths,
    "total_time": total_time
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')