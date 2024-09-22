import json
import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

N = len(west_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Create the LP problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Variables
time_vars = pulp.LpVariable.dicts("time", (range(N), range(W)), lowBound=0)

# Objective function
problem += time_vars[0][0], "Total Travel Time"

# Constraints for moving through the grid
for n in range(N):
    for w in range(W):
        if n == 0 and w == 0:
            continue  # Starting point
        if w > 0:
            problem += time_vars[n][w] >= time_vars[n][w-1] + west_time[n][w-1]
        if n > 0:
            problem += time_vars[n][w] >= time_vars[n-1][w] + north_time[n-1][w]

# Get the total travel time
total_time = time_vars[N-1][W-1]
problem += total_time  # Set the objective to minimize total time

# Solve the problem
problem.solve()

# Backtrack to find the path
paths = []
n, w = N - 1, W - 1

while n > 0 or w > 0:
    paths.append((n, w))
    if w > 0 and (n == 0 or time_vars[n][w].value() == time_vars[n][w-1].value() + west_time[n][w-1]):
        w -= 1
    else:
        n -= 1

paths.append((0, 0))  # Add the starting point
paths.reverse()  # To get the path from start to end

# Output the results
total_travel_time = pulp.value(problem.objective)
paths_output = [(street + 1, avenue + 1) for street, avenue in paths]  # Convert to 1-based indexing

output = {
    "paths": paths_output,
    "total_time": total_travel_time
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')