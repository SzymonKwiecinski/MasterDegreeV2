import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract data from json
west_time = data['west_time']
north_time = data['north_time']
N = len(west_time)  # Number of streets (rows)
W = len(west_time[0]) + 1  # Number of avenues (columns)

# Define the problem
problem = pulp.LpProblem("Delivery_Person_Path", pulp.LpMinimize)

# Decision Variables
# x[n][w] = 1 if the person is at intersection (w, n)
x = pulp.LpVariable.dicts("x", (range(N), range(W)), 0, 1, pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(x[0][0] * 0)  # Start point has no cost (time)
for n in range(N):
    for w in range(W):
        if w < W - 1:  # west move
            problem += pulp.lpSum(x[n][w] for n in range(N)) <= pulp.lpSum(x[n][w + 1] * west_time[n][w] for n in range(N))
        if n < N - 1:  # north move
            problem += pulp.lpSum(x[n][w] for w in range(W)) <= pulp.lpSum(x[n + 1][w] * north_time[n][w] for w in range(W))

# Constraints
# Start at (0,0)
problem += x[0][0] == 1
# End at (N-1, W-1)
problem += pulp.lpSum(x[N-1][W-1]) == 1

# Solve the problem
problem.solve()

# Extract the paths taken
paths = []
for n in range(N):
    for w in range(W):
        if x[n][w].value() == 1:
            paths.append((n+1, w+1))

# Calculate total time taken
total_time = pulp.value(problem.objective)

# Output the results
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')