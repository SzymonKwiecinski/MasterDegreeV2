import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Constants based on the input data
north_time = data['north_time']
west_time = data['west_time']
N = len(north_time) + 1  # Number of north intersections (including destination)
W = len(west_time[0]) + 1  # Number of west intersections (including destination)

# Create a linear programming problem
problem = pulp.LpProblem("Delivery_Time_Minimization", pulp.LpMinimize)

# Decision Variables: time taken to reach each intersection
time_vars = pulp.LpVariable.dicts("Time", (range(N), range(W)), lowBound=0, cat='Continuous')

# Objective: Minimize the time taken to reach the intersection (N-1, W-1)
problem += time_vars[N-1][W-1]

# Constraints
# Fill constraints for moving north and west
for n in range(N):
    for w in range(W):
        if n > 0:
            problem += time_vars[n][w] >= time_vars[n-1][w] + north_time[n-1][w]  # Coming from the south
        if w > 0:
            problem += time_vars[n][w] >= time_vars[n][w-1] + west_time[n][w-1]  # Coming from the west

# Starting point (1,1)
problem += time_vars[0][0] == 0  # Start at (1,1) with no initial time

# Solve the problem
problem.solve()

# Extract the path
total_time = pulp.value(problem.objective)
paths = []
n, w = 0, 0

# Traceback the path
while (n < N-1 or w < W-1):
    if n < N-1 and (w == W-1 or 
                    time_vars[n][w] == time_vars[n+1][w] + north_time[n][w]):
        paths.append((n + 1, w + 1))  # Move north
        n += 1
    else:
        paths.append((n + 1, w + 1))  # Move west
        w += 1

# Output result
result = {"paths": paths, "total_time": total_time}
print(json.dumps(result))

print(f' (Objective Value): <OBJ>{total_time}</OBJ>')