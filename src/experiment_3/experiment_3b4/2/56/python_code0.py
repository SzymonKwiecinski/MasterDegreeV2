import pulp

# Data
west_time = [[3.5, 4.5], [4, 4], [5, 4]]
north_time = [[10, 10, 9], [9, 9, 12]]

# Indices
N = len(west_time)
W = len(west_time[0]) + 1  # Plus one to account for the west end

# Problem
problem = pulp.LpProblem("Delivery_Route_Optimization", pulp.LpMinimize)

# Decision Variables
x_west = pulp.LpVariable.dicts("x_west", ((n, w) for n in range(N) for w in range(W-1)), cat='Binary')
x_north = pulp.LpVariable.dicts("x_north", ((n, w) for n in range(N-1) for w in range(W)), cat='Binary')

# Objective Function
problem += pulp.lpSum(west_time[n][w] * x_west[(n, w)] for n in range(N) for w in range(W-1)) + \
           pulp.lpSum(north_time[n][w] * x_north[(n, w)] for n in range(N-1) for w in range(W))

# Constraints
# Start at the first intersection
problem += x_west[(0, 0)] + x_north[(0, 0)] == 1

# Ensure the endpoint is reached by moving west
problem += x_west[(N-1, W-2)] == 1

# Flow conservation
for n in range(N):
    for w in range(W):
        west_sum = x_west[(n, w-1)] if w > 0 else 0
        north_sum = x_north[(n-1, w)] if n > 0 else 0
        problem += west_sum + north_sum == 1 if w < W-1 and n < N-1 else None

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')