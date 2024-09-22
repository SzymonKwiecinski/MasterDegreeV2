import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting dimensions
N = len(data['north_time']) + 1  # number of north streets
W = len(data['west_time'][0]) + 1  # number of west avenues

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Delivery_Time", pulp.LpMinimize)

# Decision Variables
# x[n][w] = time taken to reach the intersection of (street n, avenue w)
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N + 1) for w in range(1, W + 1)), lowBound=0)

# Objective Function
# The time to reach the last intersection (N, W) is the objective
problem += x[N, W], "Total_Time"

# Constraints
# Initialize the first intersection
problem += x[1, 1] == 0, "Start_Point"

# Fill constraints for moving north and west
for n in range(1, N + 1):
    for w in range(1, W + 1):
        if n > 1:  # can move north
            problem += x[n, w] >= x[n - 1, w] + data['north_time'][n - 2][w - 1], f"North_Move_{n}_{w}"
        if w > 1:  # can move west
            problem += x[n, w] >= x[n, w - 1] + data['west_time'][n - 1][w - 2], f"West_Move_{n}_{w}"

# Solve the problem
problem.solve()

# Collecting paths
paths = []
current_n, current_w = N, W

while current_n > 1 or current_w > 1:
    if current_n > 1 and (current_w == 1 or x[current_n, current_w].value() == x[current_n - 1, current_w].value() + data['north_time'][current_n - 2][current_w - 1]):
        paths.append((current_n - 1, current_w))
        current_n -= 1
    else:
        paths.append((current_n, current_w - 1))
        current_w -= 1

# Since we built the path backwards, reverse it
paths.reverse()

# Output the results
total_time = pulp.value(problem.objective)
output = {
    "paths": paths,
    "total_time": total_time
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')