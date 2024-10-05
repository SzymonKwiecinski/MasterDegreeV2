import pulp

# Data
west_time = [[3.5, 4.5], [4, 4], [5, 4]]
north_time = [[10, 10, 9], [9, 9, 12]]

N = len(north_time) + 1  # Number of rows
W = len(west_time[0]) + 1  # Number of columns

# Problem
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Decision Variables
x_N = pulp.LpVariable.dicts("x_N", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
x_W = pulp.LpVariable.dicts("x_W", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective Function
problem += pulp.lpSum(north_time[n - 1][w - 1] * x_N[(n, w)] for n in range(1, N) for w in range(1, W)) + \
           pulp.lpSum(west_time[n - 1][w - 1] * x_W[(n, w)] for n in range(1, N) for w in range(1, W))

# Constraints
problem += pulp.lpSum(x_W[(1, w)] for w in range(1, W)) == 1  # Start moving West
problem += pulp.lpSum(x_N[(n, 1)] for n in range(1, N)) == 1  # Start moving North

m = N + W - 2  # Total stages for movement
problem += pulp.lpSum(x_W[(N - 1, w)] for w in range(1, W)) + pulp.lpSum(x_N[(n, W - 1)] for n in range(1, N)) == m

for n in range(1, N):
    for w in range(1, W):
        problem += x_N[(n, w)] + x_W[(n, w)] == 1

# Solve
problem.solve()

# Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')