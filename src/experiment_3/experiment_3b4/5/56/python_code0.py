import pulp

# Data from the problem
west_time = [[3.5, 4.5], [4, 4], [5, 4]]
north_time = [[10, 10, 9], [9, 9, 12]]

# Dimensions from the data
N = len(north_time) + 1 # Number of rows
W = len(west_time[0]) + 1 # Number of columns

# Define the LP problem
problem = pulp.LpProblem("ShortestPath", pulp.LpMinimize)

# Define the decision variables
x_north = pulp.LpVariable.dicts("x_north", ((n, w) for n in range(1, N) for w in range(1, W + 1)), cat="Binary")
x_west = pulp.LpVariable.dicts("x_west", ((n, w) for n in range(1, N + 1) for w in range(1, W)), cat="Binary")

# Objective function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * x_west[n, w] for n in range(1, N+1) for w in range(1, W))
    + pulp.lpSum(north_time[n-1][w-1] * x_north[n, w] for n in range(1, N) for w in range(1, W+1))
)

# Constraints
problem += x_north[1, 1] + x_west[1, 1] == 1, "StartAt_1_1"

problem += x_north[N-1, W] == 1, "EndAt_N_W"

for n in range(2, N):
    for w in range(2, W):
        problem += (
            x_north[n-1, w] + x_west[n, w-1] == x_north[n, w] + x_west[n, w],
            f"FlowConservation_{n}_{w}"
        )

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')