import pulp
import json

# Data input
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

N = len(west_time) + 1  # number of streets (rows)
W = len(west_time[0]) + 1  # number of avenues (columns)

# Create the problem
problem = pulp.LpProblem("Delivery_Problem", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("Path", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective function
problem += pulp.lpSum(
    (north_time[n][w] * x[(n, w)] if n < N - 1 and w < W else 0) + 
    (west_time[n][w] * x[(n, w)] if n < N and w < W - 1 else 0)
    for n in range(N) for w in range(W)
), "Total_Time"

# Constraints
# Start point
problem += x[(0, 0)] == 1, "Start"

# End point
problem += pulp.lpSum(x[(N - 1, w)] for w in range(W)) == 1, "End_Street"
problem += pulp.lpSum(x[(n, W - 1)] for n in range(N)) == 1, "End_Avenue"

# Flow balance - for each intersection (except the start and end points)
for n in range(N):
    for w in range(W):
        if not (n == 0 and w == 0) and not (n == N - 1 and w == W - 1):
            problem += pulp.lpSum(x[(n, w)] for n in range(N)) == \
                       pulp.lpSum(x[(n, w)] for w in range(W)), "Flow_Balance_({}, {})".format(n, w)

# Solve the problem
problem.solve()

# Extract results
total_time = pulp.value(problem.objective)
paths = [(n, w) for n in range(N) for w in range(W) if pulp.value(x[(n, w)]) == 1]

# Output
output = {
    "paths": paths,
    "total_time": total_time
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')