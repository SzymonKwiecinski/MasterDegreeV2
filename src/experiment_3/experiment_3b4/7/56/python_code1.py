import pulp

# Load data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1
W = len(west_time[0]) + 1

# Create the problem
problem = pulp.LpProblem("Path_Optimization", pulp.LpMinimize)

# Create decision variables
x_west = pulp.LpVariable.dicts("x_west", ((n, w) for n in range(1, N + 1) for w in range(1, W)), cat='Binary')
x_north = pulp.LpVariable.dicts("x_north", ((n, w) for n in range(1, N) for w in range(1, W + 1)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * x_west[n, w] for n in range(1, N + 1) for w in range(1, W) if n <= len(west_time) and w <= len(west_time[0])) +
    pulp.lpSum(north_time[n-1][w-1] * x_north[n, w] for n in range(1, N) for w in range(1, W + 1) if n <= len(north_time) and w <= len(north_time[0]))
)

# Constraints

# Starting point
problem += x_west[1, 1] + x_north[1, 1] == 1

# Interior intersections
for n in range(2, N + 1):
    for w in range(2, W + 1):
        prev_north = x_north[n-1, w] if (n-1, w) in x_north else 0
        prev_west = x_west[n, w-1] if (n, w-1) in x_west else 0
        if (n, w) in x_north and (n, w) in x_west:
            problem += prev_north + prev_west == x_north[n, w] + x_west[n, w]

# Destination point
problem += x_west[N, W-1] + x_north[N-1, W] == 1

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')