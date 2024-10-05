import pulp
import json

# Data provided in JSON format
data_json = '{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}'
data = json.loads(data_json)

# Parameters
west_time = data['west_time']
north_time = data['north_time']
N = len(north_time) + 1  # Since north_time has N-1 entries
W = len(west_time[0]) + 1  # Since west_time has W-1 entries

# Create the problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Decision Variables
x_N = pulp.LpVariable.dicts("x_N", ((n, w) for n in range(1, N+1) for w in range(1, W+1)), cat='Binary')
x_W = pulp.LpVariable.dicts("x_W", ((n, w) for n in range(1, N+1) for w in range(1, W+1)), cat='Binary')

# Objective Function
problem += pulp.lpSum(west_time[n-1][w-1] * x_W[n, w] for n in range(1, N+1) for w in range(1, W)) + \
           pulp.lpSum(north_time[n-1][w-1] * x_N[n, w] for n in range(1, N) for w in range(1, W+1))

# Constraints
problem += pulp.lpSum(x_W[1, w] for w in range(1, W)) + pulp.lpSum(x_N[n, 1] for n in range(1, N)) == 1  # Start at (1,1)
problem += pulp.lpSum(x_W[N, w] for w in range(1, W)) + pulp.lpSum(x_N[n, W] for n in range(1, N)) == 1  # End at (N,W)

# Each intersection decision variables constraint
for n in range(1, N+1):
    for w in range(1, W+1):
        problem += x_N[n, w] + x_W[n, w] == 1  # You must move north or west

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')