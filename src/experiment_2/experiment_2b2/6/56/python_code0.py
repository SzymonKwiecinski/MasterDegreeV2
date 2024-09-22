import pulp

# Define the data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Extract data
west_time = data['west_time']
north_time = data['north_time']

# Dimensions
N = len(west_time)
W = len(west_time[0]) + 1

# Initialize the problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Variables for each path decision
north_vars = pulp.LpVariable.dicts("North", ((n, w) for n in range(N-1) for w in range(W)), lowBound=0, cat='Binary')
west_vars = pulp.LpVariable.dicts("West", ((n, w) for n in range(N) for w in range(W-1)), lowBound=0, cat='Binary')

# Objective function: minimize the total time
problem += pulp.lpSum(west_time[n][w] * west_vars[n, w] for n in range(N) for w in range(W-1)) + \
           pulp.lpSum(north_time[n][w] * north_vars[n, w] for n in range(N-1) for w in range(W))

# Constraints
for n in range(N):
    for w in range(W):
        if n == 0 and w == 0:
            problem += (pulp.lpSum(west_vars[n, w] for w in range(W-1)) + pulp.lpSum(north_vars[n, w] for w in range(W))) == 1
        elif n == N-1 and w == W-1:
            problem += (pulp.lpSum(west_vars[n, w] for w in range(W-1)) + pulp.lpSum(north_vars[n, w] for w in range(W))) == -1
        else:
            incoming = 0
            if n > 0:
                incoming += north_vars[n-1, w]
            if w > 0:
                incoming += west_vars[n, w-1]
            outgoing = 0
            if n < N-1:
                outgoing += north_vars[n, w]
            if w < W-1:
                outgoing += west_vars[n, w]
            problem += incoming - outgoing == 0

# Solve the problem
problem.solve()

# Extract the solution
paths = []
for n in range(N):
    for w in range(W-1):
        if pulp.value(west_vars[n, w]) > 0.5:
            paths.append((n + 1, w + 1))
for n in range(N-1):
    for w in range(W):
        if pulp.value(north_vars[n, w]) > 0.5:
            paths.append((n + 1, w + 1))

total_time = pulp.value(problem.objective)

# Output
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')