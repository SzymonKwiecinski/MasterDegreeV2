import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting dimensions
N = len(data['west_time'])  # number of north streets
W = len(data['west_time'][0]) + 1  # number of avenues (W-1 blocks in west_time)
M = N + W - 2  # total moves required (N-1 north and W-1 west)

# Create the LP problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Decision variables for the path taken (n, w)
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective function: minimize the total time
total_time = pulp.lpSum(x[n, w] * (data['north_time'][n][w] if n < N-1 else 0) +
                        x[n, w] * (data['west_time'][n][w-1] if w > 0 else 0) 
                        for n in range(N) for w in range(W))
problem += total_time

# Constraints
# Starting point
problem += x[0, 0] == 1  # Start at (0, 0)

# End point
problem += pulp.lpSum(x[N-1, w] for w in range(W)) == 1  # End at the last row
problem += pulp.lpSum(x[n, W-1] for n in range(N)) == 1  # End at the last column

# Induction constraints for movement
for n in range(N):
    for w in range(W):
        if n < N - 1:
            problem += x[n, w] <= pulp.lpSum(x[n + 1, w]), "North_Constraint_%d_%d" % (n, w)
        if w > 0:
            problem += x[n, w] <= pulp.lpSum(x[n, w - 1]), "West_Constraint_%d_%d" % (n, w)

# Solve the problem
problem.solve()

# Extracting the paths and total time
paths = [(n + 1, w + 1) for n in range(N) for w in range(W) if pulp.value(x[n, w]) == 1]
total_travel_time = pulp.value(problem.objective)

# Output in the required format
output = {
    "paths": paths,
    "total_time": total_travel_time
}

# Print required objective value
print(f' (Objective Value): <OBJ>{total_travel_time}</OBJ>')