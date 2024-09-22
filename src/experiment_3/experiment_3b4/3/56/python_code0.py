import pulp

# Data from JSON
west_time = [[3.5, 4.5], [4, 4], [5, 4]]
north_time = [[10, 10, 9], [9, 9, 12]]

# Dimensions
N = len(north_time) + 1
W = len(west_time[0]) + 1

# Initialize the problem
problem = pulp.LpProblem("ShortestPath", pulp.LpMinimize)

# Decision variables
x_N = pulp.LpVariable.dicts("x_N", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
x_W = pulp.LpVariable.dicts("x_W", ((n, w) for n in range(1, N+1) for w in range(1, W)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum([x_N[n, w] * north_time[n-1][w-1] for n in range(1, N) for w in range(1, W)]) +
    pulp.lpSum([x_W[n, w] * west_time[n-1][w-1] for n in range(1, N) for w in range(1, W-1)])
)

# Constraints
problem += x_N[1, 1] + x_W[1, 1] == 1  # Starting point

# Flow constraints
for n in range(2, N):
    for w in range(2, W):
        problem += (pulp.lpSum(x_N[n-1, w] for n in range(2, N)) + 
                    pulp.lpSum(x_W[n, w-1] for w in range(2, W)) ==
                    x_N[n, w] + x_W[n, w])

# Ending point constraints
problem += x_N[N-1, W-1] == 0
problem += x_W[N-1, W-1] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')