import pulp

# Data
west_time = [[3.5, 4.5], [4, 4], [5, 4]]
north_time = [[10, 10, 9], [9, 9, 12]]

N = len(north_time) + 1
W = len(west_time[0]) + 1

# Initialize the problem
problem = pulp.LpProblem("Path_Optimization", pulp.LpMinimize)

# Decision variables
x_north = pulp.LpVariable.dicts("x_north", (range(1, N), range(1, W+1)), cat='Binary')
x_west = pulp.LpVariable.dicts("x_west", (range(1, N+1), range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum(west_time[n-1][w-1] * x_west[n][w] for n in range(1, N+1) for w in range(1, W)) + \
           pulp.lpSum(north_time[n-1][w-1] * x_north[n][w] for n in range(1, N) for w in range(1, W+1))

# Constraints
for n in range(1, N):
    for w in range(1, W):
        if (n, w) != (N-1, W-1):
            problem += x_north[n][w] + x_west[n][w] == 1

problem += x_north[1][1] + x_west[1][1] == 1

problem += x_north[N-1][W] == 0
problem += x_west[N][W-1] == 0

for n in range(1, N):
    for w in range(1, W):
        problem += x_north[n][w] <= 1
        problem += x_west[n][w] <= 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')