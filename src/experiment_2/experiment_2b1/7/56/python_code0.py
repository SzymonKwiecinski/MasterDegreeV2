import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

W = len(data['west_time'][0]) + 1  # Number of avenues
N = len(data['north_time']) + 1     # Number of streets

# Create the LP problem
problem = pulp.LpProblem("Delivery_Time_Minimization", pulp.LpMinimize)

# Decision variables
# Use dictionaries to store the variables for the paths
north_vars = pulp.LpVariable.dicts("North", ((n, w) for n in range(N - 1) for w in range(W)), cat='Binary')
west_vars = pulp.LpVariable.dicts("West", ((n, w) for n in range(N) for w in range(W - 1)), cat='Binary')

# Objective function: Minimizing total time
total_time = pulp.lpSum(north_vars[n, w] * data['north_time'][n][w] for n in range(N - 1) for w in range(W)) + \
             pulp.lpSum(west_vars[n, w] * data['west_time'][n][w] for n in range(N) for w in range(W - 1))

problem += total_time

# Constraints to ensure one decision at each intersection
for n in range(N):
    for w in range(W):
        if n < N - 1 and w < W - 1:
            problem += (north_vars[n, w] + west_vars[n, w] == 1, f"Stage_{n}_{w}")

# Ensure to start at (0,0) and end at (N-1, W-1)
problem += (pulp.lpSum(west_vars[0, w] for w in range(W - 1)) == 1, "Start_Condition")
problem += (pulp.lpSum(north_vars[n, 0] for n in range(N - 1)) == 1, "Start_Condition_North")

# Solve the problem
problem.solve()

# Collect the paths taken
paths = []
for n in range(N - 1):
    for w in range(W):
        if north_vars[n, w].varValue > 0:
            paths.append((n + 2, w + 1))  # +2 and +1 to adjust for 1-based indexing
for n in range(N):
    for w in range(W - 1):
        if west_vars[n, w].varValue > 0:
            paths.append((n + 1, w + 2))  # +1 and +2 to adjust for 1-based indexing

# Total travel time
total_travel_time = pulp.value(problem.objective)

# Output the results
output = {
    "paths": paths,
    "total_time": total_travel_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')