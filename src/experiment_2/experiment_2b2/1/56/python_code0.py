import pulp

# Load the data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1
W = len(west_time[0]) + 1

# Create the LP problem
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Decision variables: x_nw (move west), y_nw (move north)
x_vars = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N+1) for w in range(1, W)), cat='Binary')
y_vars = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N+1) for w in range(1, W+1)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * x_vars[(n, w)] for n in range(1, N+1) for w in range(1, W)) +
    pulp.lpSum(north_time[n-1][w-1] * y_vars[(n, w)] for n in range(1, N) for w in range(1, W+1))
)

# Constraints
# Start at (1, 1)
problem += x_vars[(1, 1)] + y_vars[(1, 1)] == 1

# End at (N, W)
problem += x_vars[(N, W-1)] + y_vars[(N-1, W)] == 1

# Flow conservation
for n in range(1, N+1):
    for w in range(1, W+1):
        if n == 1 and w == 1:
            continue
        if n == N and w == W:
            continue

        inflow = (x_vars[(n, w-1)] if w > 1 else 0) + (y_vars[(n-1, w)] if n > 1 else 0)
        outflow = (x_vars[(n, w)] if w < W else 0) + (y_vars[(n, w)] if n < N else 0)
        
        problem += inflow == outflow

# Solve the problem
problem.solve()

# Extract the solution
paths = []
for n in range(1, N+1):
    for w in range(1, W):
        if pulp.value(x_vars[(n, w)]) == 1:
            paths.append((n, w))
for n in range(1, N):
    for w in range(1, W+1):
        if pulp.value(y_vars[(n, w)]) == 1:
            paths.append((n, w))

total_time = pulp.value(problem.objective)

# Output the result
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')