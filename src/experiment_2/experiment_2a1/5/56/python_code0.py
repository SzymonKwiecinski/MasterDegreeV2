import json
import pulp

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract the grid dimensions
N = len(data['north_time']) + 1
W = len(data['west_time'][0]) + 1

# Create the optimization problem
problem = pulp.LpProblem("Delivery_Problem", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("x", 
                            ((n, w) for n in range(N) for w in range(W)), 
                            lowBound=0, 
                            cat='Binary')

# Objective function: minimize total walking time
problem += pulp.lpSum(x[n, w] * (data['north_time'][n-1][w] if n > 0 else 0) for n in range(N) for w in range(W) if n > 0) + \
                      pulp.lpSum(x[n, w] * (data['west_time'][n][w-1] if w > 0 else 0) for n in range(N) for w in range(W) if w > 0)

# Constraints to ensure one path from start (0,0) to end (N-1,W-1)
problem += pulp.lpSum(x[0, 0]) == 1  # Start at (0,0)
problem += pulp.lpSum(x[N-1, W-1]) == 1  # End at (N-1, W-1)

# Flow conservation constraints
for n in range(N):
    for w in range(W):
        if n > 0:
            problem += pulp.lpSum(x[n, w] for n in range(N) if n > 0) == \
                       pulp.lpSum(x[n-1, w] for n in range(N) if n < N)
        if w > 0:
            problem += pulp.lpSum(x[n, w] for w in range(W) if w > 0) == \
                       pulp.lpSum(x[n, w-1] for w in range(W) if w < W)

# Solve the problem
problem.solve()

# Collect paths and total time
paths = [(n, w) for n in range(N) for w in range(W) if pulp.value(x[n, w]) == 1]
total_time = pulp.value(problem.objective)

# Prepare output
output = {
    "paths": paths,
    "total_time": total_time
}

# Print results
print(output)
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')