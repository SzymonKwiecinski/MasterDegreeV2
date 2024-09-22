import pulp
import json

# Data input from JSON format
data_json = '''
{
    "west_time": [[3.5, 4.5], [4, 4], [5, 4]], 
    "north_time": [[10, 10, 9], [9, 9, 12]]
}
'''
data = json.loads(data_json)

# Dimensions of the grid
N = len(data['north_time']) + 1  # Number of streets
W = len(data['west_time'][0]) + 1  # Number of avenues

# Create a linear programming problem
problem = pulp.LpProblem("Optimal_Path", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", (range(1, N + 1), range(1, W + 1)), cat='Binary')

# Objective function: total travel time
total_time = pulp.lpSum(
    (data['west_time'][n - 1][w - 1] * x[n][w] if w < W else 0) + 
    (data['north_time'][n - 1][w - 1] * x[n][w] if n < N else 0)
    for n in range(1, N + 1) for w in range(1, W + 1)
)

problem += total_time, "Total_Travel_Time"

# Constraints
# Start from (1, 1)
problem += x[1][1] == 1, "Start"

# End at (N, W)
problem += x[N][W] == 1, "End"

# Ensure continuity
for n in range(1, N + 1):
    problem += pulp.lpSum(x[n][w] for w in range(1, W + 1)) - \
               pulp.lpSum(x[n + 1][w] for w in range(1, W + 1)) == 0 if n < N else None

for w in range(1, W + 1):
    problem += pulp.lpSum(x[n][w] for n in range(1, N + 1)) - \
               pulp.lpSum(x[n][w + 1] for n in range(1, N + 1)) == 0 if w < W else None

# Solve the problem
problem.solve()

# Extract the path
path = [(n, w) for n in range(1, N + 1) for w in range(1, W + 1) if pulp.value(x[n][w]) == 1]

# Total travel time
total_travel_time = pulp.value(problem.objective)

# Prepare output
output = {
    "paths": path,
    "total_time": total_travel_time
}

# Display the objective value
print(f' (Objective Value): <OBJ>{total_travel_time}</OBJ>')