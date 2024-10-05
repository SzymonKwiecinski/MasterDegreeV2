import pulp
import json

# Load the data from JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

# Define dimensions based on the data
N = len(north_time) + 1  # number of rows (including the starting position)
W = len(west_time[0]) + 1  # number of columns (including the starting position)

# Create the problem instance
problem = pulp.LpProblem("Delivery_Path_Optimization", pulp.LpMinimize)

# Define decision variables
x_nw_N = pulp.LpVariable.dicts("x_nw_N", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
x_nw_W = pulp.LpVariable.dicts("x_nw_W", ((n, w) for n in range(1, N) for w in range(1, W-1)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * x_nw_W[(n, w)] for n in range(1, N) for w in range(1, W-1)) +
    pulp.lpSum(north_time[n-1][w-1] * x_nw_N[(n, w)] for n in range(1, N-1) for w in range(1, W))
)

# Constraints
for n in range(1, N):
    for w in range(1, W):
        if (n, w) in x_nw_N and (n, w) in x_nw_W:  # Ensure the key exists
            problem += x_nw_N[(n, w)] + x_nw_W[(n, w)] == 1  # Movement constraint

for w in range(1, W):
    problem += pulp.lpSum(x_nw_N[(n, w)] for n in range(1, N-1)) == pulp.lpSum(x_nw_N[(n+1, w)] for n in range(0, N-2))  # North flow conservation

for n in range(1, N):
    problem += pulp.lpSum(x_nw_W[(n, w)] for w in range(1, W-1)) == pulp.lpSum(x_nw_W[(n, w+1)] for w in range(1, W-2))  # West flow conservation

problem += x_nw_N[(1, 1)] + x_nw_W[(1, 1)] == 1  # Starting position constraint

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')