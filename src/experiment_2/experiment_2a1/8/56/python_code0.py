import json
import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']
N = len(west_time)  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Create a linear programming problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(W)), cat='Binary')

# Objective function: Minimize total time
problem += pulp.lpSum(north_time[n][w] * x[n][w] for n in range(N-1) for w in range(W)) + \
           pulp.lpSum(west_time[n][w] * x[n][w] for n in range(N) for w in range(W-1))

# Constraints
# Start point
problem += x[0][0] == 1  # Start at (1st Street, 1st Avenue)

# End point
problem += pulp.lpSum(x[N-1][w] for w in range(W)) == 1  # End at (Nth Street, Wth Avenue)
problem += pulp.lpSum(x[n][W-1] for n in range(N)) == 1  # End at (Nth Street, Wth Avenue)

# Flow conservation constraints
for n in range(N):
    for w in range(W):
        if n < N-1:  # North flow
            problem += x[n][w] - x[n+1][w] >= 0
        if w < W-1:  # West flow
            problem += x[n][w] - x[n][w+1] >= 0

# Solve the problem
problem.solve()

# Collect paths
paths = [(n + 1, w + 1) for n in range(N) for w in range(W) if pulp.value(x[n][w]) == 1]

# Total time taken
total_time = pulp.value(problem.objective)

# Output
output = {
    "paths": paths,
    "total_time": total_time
}

# Print output
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')