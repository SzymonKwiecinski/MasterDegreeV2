import pulp
import json

# Data parsed from JSON format
data = json.loads("{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}")
west_time = data['west_time']
north_time = data['north_time']

# Dimensions
N = len(north_time) + 1  # since north_time is for N-1
W = len(west_time[0]) + 1  # since west_time is for W-1

# Create the problem
problem = pulp.LpProblem("Delivery_Path_Optimization", pulp.LpMinimize)

# Define decision variables
x_west = pulp.LpVariable.dicts("x_west", ((n, w) for n in range(1, N+1) for w in range(1, W)), cat='Binary')
x_north = pulp.LpVariable.dicts("x_north", ((n, w) for n in range(1, N) for w in range(1, W+1)), cat='Binary')

# Objective function
problem += pulp.lpSum(west_time[n-1][w-1] * x_west[(n, w)] for n in range(1, N+1) for w in range(1, W)) + \
           pulp.lpSum(north_time[n-1][w-1] * x_north[(n, w)] for n in range(1, N) for w in range(1, W+1))

# Constraints
# Start at (1,1)
problem += x_west[(1, 1)] + x_north[(1, 1)] == 1

# End at (N,W)
problem += x_west[(N, W-1)] + x_north[(N-1, W)] == 1

# Flow conservation for each internal node
for n in range(2, N):
    for w in range(2, W):
        problem += x_west[(n, w)] + x_north[(n, w)] == x_north[(n-1, w)] + x_west[(n, w-1)]

# Boundary conditions
for n in range(2, N):
    problem += x_north[(n, 1)] == x_north[(n-1, 1)]
    
for w in range(2, W):
    problem += x_west[(1, w)] == x_west[(1, w-1)]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')