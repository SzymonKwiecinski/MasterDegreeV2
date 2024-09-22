import json
import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting west_time and north_time from the provided data
west_time = data['west_time']
north_time = data['north_time']
N = len(west_time)  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues (W = len(west_time[0]) + 1)
# Create the problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective function
problem += pulp.lpSum(north_time[n][w] * x[(n, w)] for n in range(N - 1) for w in range(W)) + pulp.lpSum(west_time[n][w] * x[(n, w)] for n in range(N) for w in range(W - 1))

# Constraints

# Starting point
problem += pulp.lpSum(x[(0, w)] for w in range(W)) == 1  # Start at the first avenue

# Ending point
problem += pulp.lpSum(x[(N-1, w)] for w in range(W)) == 1  # End at the last avenue

# Ensure that we do not leave intersections
for n in range(N):
    for w in range(W):
        if n < N - 1:  # Moving north
            problem += x[(n, w)] <= pulp.lpSum(x[(n + 1, w)] for n in range(n, N)) # Can only leave if we go north
        if w < W - 1:  # Moving west
            problem += x[(n, w)] <= pulp.lpSum(x[(n, w + 1)] for w in range(w, W)) # Can only leave if we go west

# Solve the problem
problem.solve()

# Collecting paths
paths = []
total_travel_time = pulp.value(problem.objective)

for n in range(N):
    for w in range(W):
        if pulp.value(x[(n, w)]) == 1:
            paths.append((n + 1, w + 1))

# Output result
output = {
    "paths": paths,
    "total_time": total_travel_time
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{total_travel_time}</OBJ>')