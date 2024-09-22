import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

# Define the dimensions
N = len(west_time) + 1  # number of streets (rows)
W = len(west_time[0]) + 1  # number of avenues (columns)

# Create the linear programming problem
problem = pulp.LpProblem("Delivery_Problem", pulp.LpMinimize)

# Create decision variables
time_vars = pulp.LpVariable.dicts("Time", [(n, w) for n in range(N) for w in range(W)], lowBound=0)

# Objective function: minimize total time
problem += time_vars[0, 0], "Total_Travel_Time"

# Constraints for moving in the grid (initial condition)
for w in range(W):
    problem += time_vars[0, w] == pulp.lpSum(north_time[0][w] for n in range(1)) if w > 0 else 0

for n in range(N):
    problem += time_vars[n, 0] == pulp.lpSum(west_time[n][0] for n in range(1)) if n > 0 else 0

# Constraints for moving north or west
for n in range(N):
    for w in range(W):
        if n > 0:
            problem += time_vars[n, w] >= time_vars[n-1, w] + north_time[n-1][w]  # Moving north
        if w > 0:
            problem += time_vars[n, w] >= time_vars[n, w-1] + west_time[n][w-1]  # Moving west

# Solve the problem
problem.solve()

# Collecting paths for output
paths = []
total_time = pulp.value(problem.objective)

# Create the result dictionary
result = {
    "paths": paths,
    "total_time": total_time
}

print(f' (Objective Value): <OBJ>{result["total_time"]}</OBJ>')