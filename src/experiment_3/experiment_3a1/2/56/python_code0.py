import pulp
import json

# Data
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

# Parameters
W = len(west_time[0]) + 1  # Number of Avenues
N = len(north_time) + 1    # Number of Streets

# Create the problem
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", (range(1, N), range(1, W)), cat='Binary')

# Objective Function
problem += pulp.lpSum(west_time[n-1][w-1] * x[n][w] + north_time[n-1][w-1] * x[n][w] for n in range(1, N) for w in range(1, W)), "TotalTravelTime"

# Constraints
# Moving North or West
for n in range(1, N):
    problem += pulp.lpSum(x[n][w] for w in range(1, W)) == 1, f"OnePathNorth_n{n}"

for w in range(1, W):
    problem += pulp.lpSum(x[n][w] for n in range(1, N)) == 1, f"OnePathWest_w{w}"

# Start from the first intersection
problem += x[1][1] == 1, "StartAtIntersection"

# End at the last intersection
problem += x[N-1][W-1] == 1, "EndAtIntersection"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')