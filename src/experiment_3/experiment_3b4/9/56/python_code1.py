import pulp

# Data input
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Dimensions
N = len(data['north_time']) + 1  # Number of Streets
W = len(data['west_time'][0]) + 1  # Number of Avenues

# Initialize the problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Decision Variables
x_north = pulp.LpVariable.dicts("x_north", ((n, w) for n in range(1, N) for w in range(1, W+1)), cat='Binary')
x_west = pulp.LpVariable.dicts("x_west", ((n, w) for n in range(1, N+1) for w in range(1, W)), cat='Binary')

# Objective Function
north_time_sum = pulp.lpSum(data['north_time'][n-1][w-1] * x_north[n, w] for n in range(1, N) for w in range(1, W+1))
west_time_sum = pulp.lpSum(data['west_time'][n-1][w-1] * x_west[n, w] for n in range(1, N+1) for w in range(1, W))
problem += north_time_sum + west_time_sum

# Flow Constraints
for n in range(1, N):
    for w in range(1, W):
        problem += x_north[n, w] + x_west[n, w+1] == x_north[n+1, w] + x_west[n, w]
    for w in range(1, W+1):
        problem += x_west[n, w] + x_north[n+1, w] == x_west[n, w+1] + x_north[n, w]

# Boundary Conditions
problem += x_north[1, 1] + x_west[1, 1] == 1  # Start
problem += x_north[N-1, W] + x_west[N, W-1] == 0  # End

# Solve
problem.solve()

# Print objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')