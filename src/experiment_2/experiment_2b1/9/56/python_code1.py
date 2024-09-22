import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting dimensions
N = len(data['north_time']) + 1  # Number of streets
W = len(data['west_time'][0]) + 1  # Number of avenues
west_time = data['west_time']
north_time = data['north_time']

# Define the problem
problem = pulp.LpProblem("Shortest_Path", pulp.LpMinimize)

# Decision variables for movements
x = pulp.LpVariable.dicts('x', (range(N), range(W)), lowBound=0, cat='Binary')

# Setting the objective
objective = pulp.lpSum(north_time[n][w] * x[n][w] for n in range(N-1) for w in range(W)) + \
            pulp.lpSum(west_time[n][w] * x[n][w] for n in range(N) for w in range(W-1))

problem += objective

# Constraints
# Start point
problem += x[0][0] == 1  # Start at (1,1)

# End point
problem += pulp.lpSum(x[N-1][W-1]) == 1  # End at (N,W)

# Movement constraints
for n in range(N):
    for w in range(W):
        if n > 0:  # Not the first street
            problem += x[n][w] <= pulp.lpSum(x[n-1][w] for x in range(N))  # Coming from the south
        if w > 0:  # Not the first avenue
            problem += x[n][w] <= pulp.lpSum(x[n][w-1] for y in range(W))  # Coming from the west

# Solve the problem
problem.solve()

# Extracting paths and total_time
total_time = pulp.value(problem.objective)
paths = [(n+1, w+1) for n in range(N) for w in range(W) if pulp.value(x[n][w]) == 1]

# Preparing the output
output = {
    "paths": paths,
    "total_time": total_time
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')