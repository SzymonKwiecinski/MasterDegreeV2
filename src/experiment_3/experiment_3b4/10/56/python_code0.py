import pulp

# Define the LP problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Data
west_time = [[3.5, 4.5], [4, 4], [5, 4]]
north_time = [[10, 10, 9], [9, 9, 12]]

N = len(north_time) + 1
W = len(west_time[0]) + 1

# Decision variables
x_n_w_N = pulp.LpVariable.dicts("x_n_w_N", ((n, w) for n in range(1, N) for w in range(1, W+1)),
                                cat='Binary')
x_n_w_W = pulp.LpVariable.dicts("x_n_w_W", ((n, w) for n in range(1, N+1) for w in range(1, W)),
                                cat='Binary')

# Objective function
problem += pulp.lpSum(north_time[n-1][w-1] * x_n_w_N[(n, w)] for n in range(1, N) for w in range(1, W)) + \
           pulp.lpSum(west_time[n-1][w-1] * x_n_w_W[(n, w)] for n in range(1, N) for w in range(1, W)), "Total_Travel_Time"

# Constraints

# Start at (1,1)
problem += x_n_w_W[(1, 1)] + x_n_w_N[(1, 1)] == 1, "Start_Position"

# Flow conservation
for n in range(1, N-1):
    for w in range(1, W-1):
        problem += x_n_w_W[(n, w)] + x_n_w_N[(n+1, w)] == x_n_w_W[(n, w+1)] + x_n_w_N[(n, w)], f"Flow_Conservation_{n}_{w}"

# End at (N,W)
problem += x_n_w_W[(N-1, W-1)] + x_n_w_N[(N-1, W)] == 1, "End_Position"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')