import json
import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting dimensions
N = len(data['north_time']) + 1  # Number of streets
W = len(data['west_time'][0]) + 1  # Number of avenues

# Create the Linear Program
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Decision variables for the grid
x = pulp.LpVariable.dicts("path", (range(N), range(W)), 0, 1, pulp.LpBinary)

# Objective function: Minimize total travel time
total_time = pulp.lpSum(data['west_time'][n][w] * x[n][w] for n in range(N) for w in range(W-1)) + \
             pulp.lpSum(data['north_time'][n][w] * x[n][w] for n in range(N-1) for w in range(W))
problem += total_time

# Constraints
# Start point
problem += x[0][0] == 1

# End point should be reached
problem += pulp.lpSum(x[N-1][w] for w in range(W)) == 1
problem += pulp.lpSum(x[n][W-1] for n in range(N)) == 1

# Flow conservation: Moving right (west)
for n in range(N):
    for w in range(W-1):
        problem += x[n][w] <= pulp.lpSum(x[n][w+1] for n in range(N))

# Flow conservation: Moving up (north)
for n in range(N-1):
    for w in range(W):
        problem += x[n][w] <= pulp.lpSum(x[n+1][w] for w in range(W))

# Solve the problem
problem.solve()

# Extracting the paths
paths = [(n, w) for n in range(N) for w in range(W) if pulp.value(x[n][w]) == 1]

# Extract the total travel time
total_travel_time = pulp.value(problem.objective)

# Preparing output
output = {
    "paths": paths,
    "total_time": total_travel_time
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')