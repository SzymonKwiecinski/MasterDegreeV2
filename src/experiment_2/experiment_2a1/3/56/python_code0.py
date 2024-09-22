import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting dimensions
N = len(data['west_time']) + 1  # Number of streets (north)
W = len(data['west_time'][0]) + 1  # Number of avenues (west)

# Define the problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Define decision variables for paths
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective function to minimize total time
total_time = pulp.lpSum(data['west_time'][n][w] * x[(n, w)] for n in range(N) for w in range(W-1)) + \
             pulp.lpSum(data['north_time'][n][w] * x[(n, w)] for n in range(N-1) for w in range(W))
problem += total_time

# Constraints to ensure only one path is chosen
for n in range(N):
    problem += pulp.lpSum(x[(n, w)] for w in range(W)) <= 1
for w in range(W):
    problem += pulp.lpSum(x[(n, w)] for n in range(N)) <= 1

# Starting point (1, 1)
problem += x[(0, 0)] == 1

# Ending point (N, W)
problem += pulp.lpSum(x[(N-1, w)] for w in range(W)) == 1
problem += pulp.lpSum(x[(n, W-1)] for n in range(N)) == 1

# Solve the problem
problem.solve()

# Collecting results
total_travel_time = pulp.value(problem.objective)
paths = [(n + 1, w + 1) for n in range(N) for w in range(W) if pulp.value(x[(n, w)]) == 1]

# Output format
output = {
    "paths": paths,
    "total_time": total_travel_time
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{total_travel_time}</OBJ>')