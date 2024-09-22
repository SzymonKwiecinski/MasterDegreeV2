import json
import pulp

# Input data in JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')

west_time = data['west_time']
north_time = data['north_time']

N = len(west_time)  # Number of North streets (rows)
W = len(west_time[0]) + 1  # Number of West avenues (columns)

# Create the LP problem
problem = pulp.LpProblem("Delivery_Problem", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("Path", (range(N), range(W)), cat="Binary")

# Objective function: Minimize total time
problem += pulp.lpSum(
    (north_time[n][w] * x[n][w] if n < N-1 else 0) + 
    (west_time[n][w-1] * x[n][w] if w > 0 else 0) 
    for n in range(N) for w in range(W)
)

# Constraints
# Start at (0,0)
problem += pulp.lpSum(x[0][0]) == 1

# End at (N-1,W-1)
problem += pulp.lpSum(x[N-1][W-1]) == 1

# Ensure one path from (n, w) can only lead to (n+1, w) or (n, w+1)
for n in range(N):
    for w in range(W):
        if n < N-1:
            problem += x[n][w] <= pulp.lpSum(x[n+1][w] for n in range(N))
        if w > 0:
            problem += x[n][w] <= pulp.lpSum(x[n][w-1] for w in range(W))

# Solve the problem
problem.solve()

# Extracting the total travel time and paths
total_time = pulp.value(problem.objective)
paths = [(n + 1, w) for n in range(N) for w in range(W) if pulp.value(x[n][w]) == 1]

# Output result
result = {
    "paths": paths,
    "total_time": total_time
}

print(result)
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')