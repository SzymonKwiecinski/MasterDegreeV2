import pulp
import json

# Load input data
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')

# Extract west and north times
west_time = data["west_time"]
north_time = data["north_time"]

# Get dimensions
N = len(north_time) + 1  # Streets
W = len(west_time[0]) + 1  # Avenues

# Create Problem
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', ((n, w) for n in range(N) for w in range(W)), cat='Binary')
y = pulp.LpVariable.dicts('y', ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective Function
problem += pulp.lpSum([west_time[n][w] * x[(n, w + 1)] for n in range(N) for w in range(W - 1)]) + \
           pulp.lpSum([north_time[n][w] * y[(n + 1, w)] for n in range(N - 1) for w in range(W)])

# Constraints
for n in range(N):
    for w in range(W):
        if n < N - 1 and w < W - 1:
            problem += x[(n, w + 1)] + y[(n + 1, w)] == 1

problem += x[(0, 0)] == 0
problem += y[(0, 0)] == 0

for n in range(1, N):
    problem += x[(n, 0)] == 0

for w in range(1, W):
    problem += y[(0, w)] == 0

problem += x[(N-1, W-2)] == 1
problem += y[(N-2, W-1)] == 1

# Solve Problem
problem.solve()

# Extract Results
total_time = pulp.value(problem.objective)

# Determine the optimal path
paths = []
n, w = 0, 0
while n < N - 1 or w < W - 1:
    if n < N - 1 and y[(n + 1, w)].varValue == 1:
        n += 1
    else:
        w += 1
    paths.append((n, w))

# Output
result = {
    "paths": paths,
    "total_time": total_time
}

print(json.dumps(result, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')