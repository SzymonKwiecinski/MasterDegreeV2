import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract dimensions
N = len(data['west_time'])
W = len(data['west_time'][0]) + 1  # W is one more than the number of west_time columns

# Create the LP problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Decision variable: time taken to reach each intersection (n, w)
time_vars = pulp.LpVariable.dicts("time", ((n, w) for n in range(N) for w in range(W)), lowBound=0)

# Objective function: minimize the total time to reach (N-1, W-1)
problem += time_vars[N-1, W-1], "Total_Travel_Time"

# Constraints for moving right (west)
for n in range(N):
    for w in range(W - 1):
        if w > 0 or n > 0:  # Avoid constraints for the starting point
            problem += time_vars[n, w] + data['west_time'][n][w] >= time_vars[n, w + 1]

# Constraints for moving up (north)
for n in range(N - 1):
    for w in range(W):
        if n > 0 or w > 0:  # Avoid constraints for the starting point
            problem += time_vars[n, w] + data['north_time'][n][w] >= time_vars[n + 1, w]

# Setting the starting point at (0, 0) to 0
problem += time_vars[0, 0] == 0

# Solve the problem
problem.solve()

# Extract the total_time and paths
total_time = pulp.value(problem.objective)
paths = []

# Backtrack to find the path taken based on the solution
current_n, current_w = 0, 0
while (current_n, current_w) != (N-1, W-1):
    paths.append((current_n + 1, current_w + 1))  # Convert to 1-indexed
    if current_w < W - 1 and time_vars[current_n, current_w].varValue + data['west_time'][current_n][current_w] == time_vars[current_n, current_w + 1].varValue:
        current_w += 1
    else:
        current_n += 1

# Append final point
paths.append((N, W))

# Output results
output = {
    "paths": paths,
    "total_time": total_time
}

print(f' (Objective Value): <OBJ>{output["total_time"]}</OBJ>')