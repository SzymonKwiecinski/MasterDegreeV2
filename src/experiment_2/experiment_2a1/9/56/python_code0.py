import pulp
import json

# Input data
data = json.loads("{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}")
west_time = data['west_time']
north_time = data['north_time']

# Dimensions
N = len(north_time) + 1  # Number of streets (rows)
W = len(west_time[0]) + 1  # Number of avenues (columns)

# Create the problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Decision variables: x[n][w] indicating if we move to (w,n)
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective function
problem += pulp.lpSum(north_time[n-1][w] * x[n][w] for n in range(1, N) for w in range(W)) + \
            pulp.lpSum(west_time[n][w-1] * x[n][w] for n in range(N) for w in range(1, W))

# Constraints
# To ensure we only move north or west
for n in range(N):
    for w in range(W):
        if n > 0:  # We can only move north if not at the top row
            problem += x[n][w] >= x[n-1][w]
        if w > 0:  # We can only move west if not at the leftmost column
            problem += x[n][w] >= x[n][w-1]

# Enforce starting and ending points
problem += x[0][0] == 1  # Starting point
problem += pulp.lpSum(x[N-1][W-1]) == 1  # Ending point

# Solve the problem
problem.solve()

# Retrieve the paths and total time
paths = [(n, w) for n in range(N) for w in range(W) if pulp.value(x[n][w]) == 1]
total_time = pulp.value(problem.objective)

# Output formatting
output = {
    "paths": paths,
    "total_time": total_time
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')