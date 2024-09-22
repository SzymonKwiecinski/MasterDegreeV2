import json
import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting dimensions and times
west_time = data['west_time']
north_time = data['north_time']

N = len(west_time)  # Number of streets (rows)
W = len(west_time[0]) + 1  # Number of avenues (columns)

# Create a linear programming problem
problem = pulp.LpProblem("DeliveryTimeMinimization", pulp.LpMinimize)

# Decision variables
time_vars = pulp.LpVariable.dicts("time", (range(N), range(W)), lowBound=0)

# Objective function: minimize the time to reach the bottom-right corner
problem += time_vars[N-1][W-1], "TotalTime"

# Constraints for the grid
# Fill the time for the first row (only can come from the left)
for w in range(W):
    if w == 0:
        time_vars[0][w] = west_time[0][0]  # Starting point takes the first west_time
    else:
        problem += time_vars[0][w] == time_vars[0][w-1] + west_time[0][w-1]

# Fill the time for the first column (only can come from above)
for n in range(N):
    if n == 0:
        time_vars[n][0] = 0  # Starting point has no time
    else:
        problem += time_vars[n][0] == time_vars[n-1][0] + north_time[n-1][0]

# Fill the rest of the grid
for n in range(1, N):
    for w in range(1, W):
        problem += time_vars[n][w] == pulp.lpSum([time_vars[n-1][w] + north_time[n-1][w], 
                                                    time_vars[n][w-1] + west_time[n][w-1]])

# Solve the problem
problem.solve()

# Retrieve total_time and paths
total_time = pulp.value(problem.objective)
paths = []

n, w = N - 1, W - 1

# Backtracking to find the path
while n > 0 or w > 0:
    paths.append((n + 1, w + 1))  # Store the path as 1-indexed
    if n == 0:  # Only can go west
        w -= 1
    elif w == 0:  # Only can go north
        n -= 1
    else:
        if time_vars[n][w] == time_vars[n - 1][w] + north_time[n - 1][w]:
            n -= 1
        else:
            w -= 1

# Add the start point
paths.append((1, 1))
paths.reverse()

# Output the result
result = {
    "paths": paths,
    "total_time": total_time
}

print(result)
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')