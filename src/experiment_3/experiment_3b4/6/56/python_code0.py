import pulp

# Data from JSON
west_time = [[3.5, 4.5], [4, 4], [5, 4]]
north_time = [[10, 10, 9], [9, 9, 12]]

N = len(north_time) + 1  # Number of north moves
W = len(west_time[0]) + 1  # Number of west moves

# Create the LP problem
problem = pulp.LpProblem("Delivery_Path_Optimization", pulp.LpMinimize)

# Decision variables
x_n_w_N = pulp.LpVariable.dicts("x_n_w_N", (range(1, N), range(1, W)), cat='Binary')
x_n_w_W = pulp.LpVariable.dicts("x_n_w_W", (range(1, N+1), range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum(north_time[n-1][w-1] * x_n_w_N[n][w] for n in range(1, N) for w in range(1, W)) + \
           pulp.lpSum(west_time[n-1][w-1] * x_n_w_W[n][w] for n in range(1, N+1) for w in range(1, W))

# Constraints

# Start point constraint
problem += x_n_w_W[1][1] + x_n_w_N[1][1] == 1

# End point constraint
problem += sum(x_n_w_N[N-1][w] for w in range(1, W)) + sum(x_n_w_W[n][W-1] for n in range(1, N)) == 1

# Intermediate intersections flow conservation
for n in range(1, N):
    for w in range(1, W):
        if (n, w) not in [(1, 1), (N-1, W-1)]:
            problem += (pulp.lpSum(x_n_w_N[n-1][w] for n in range(2, N) if n-1 > 0) +
                        pulp.lpSum(x_n_w_W[n][w-1] for w in range(2, W) if w-1 > 0) -
                        x_n_w_N[n][w] -
                        x_n_w_W[n][w]) == 0

# Total moves constraints
problem += pulp.lpSum(x_n_w_N[n][w] for n in range(1, N) for w in range(1, W)) == N - 1
problem += pulp.lpSum(x_n_w_W[n][w] for n in range(1, N+1) for w in range(1, W)) == W - 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')