import pulp

# Define the input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract west_time and north_time
west_time = data['west_time']
north_time = data['north_time']

# Define dimensions
N = len(north_time) + 1
W = len(west_time[0]) + 1

# Initialize the problem
problem = pulp.LpProblem("DeliveryMinTime", pulp.LpMinimize)

# Decision variables
x_north = pulp.LpVariable.dicts("North", ((n, w) for n in range(N-1) for w in range(W)), cat='Binary')
x_west = pulp.LpVariable.dicts("West", ((n, w) for n in range(N) for w in range(W-1)), cat='Binary')

# Objective function: Minimize total travel time
problem += (
    pulp.lpSum(north_time[n][w] * x_north[(n, w)] for n in range(N-1) for w in range(W)) +
    pulp.lpSum(west_time[n][w] * x_west[(n, w)] for n in range(N) for w in range(W-1))
)

# Constraints

# Start point
problem += (pulp.lpSum([x_west[(0, 0)], x_north[(0, 0)]]) == 1)

# End point
problem += (pulp.lpSum([x_west[(N-1, W-2)], x_north[(N-2, W-1)]]) == 1)

# Flow constraints
for n in range(N):
    for w in range(W):
        if n > 0:
            incoming_north = x_north[(n-1, w)] if n < N else 0
        else:
            incoming_north = 0

        if w > 0:
            incoming_west = x_west[(n, w-1)] if w < W else 0
        else:
            incoming_west = 0
            
        outgoing_north = x_north[(n, w)] if n < N-1 else 0
        outgoing_west = x_west[(n, w)] if w < W-1 else 0

        problem += (incoming_north + incoming_west - outgoing_north - outgoing_west == 0)

# Solve the problem
problem.solve()

# Retrieve the path
path = []
current_n, current_w = 0, 0

while current_n < N-1 or current_w < W-1:
    if current_n < N-1 and pulp.value(x_north[(current_n, current_w)]) == 1:
        current_n += 1
    elif current_w < W-1 and pulp.value(x_west[(current_n, current_w)]) == 1:
        current_w += 1
    path.append((current_n, current_w))

# Calculate total time
total_time = pulp.value(problem.objective)

result = {
    "paths": path,
    "total_time": total_time
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')