import pulp
import json

# Data from JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

N = len(west_time)  # Number of streets
W = len(north_time[0])  # Number of avenues

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(W-1)), cat='Binary')
y = pulp.LpVariable.dicts("y", (range(N-1), range(W)), cat='Binary')

# Objective function
problem += pulp.lpSum(x[n][w] * west_time[n][w] for n in range(N) for w in range(W-1)) + \
           pulp.lpSum(y[n][w] * north_time[n][w] for n in range(N-1) for w in range(W))

# Constraints
# Start at (1,1)
problem += pulp.lpSum(y[0][w] for w in range(W)) == 1

# End at (N,W)
problem += pulp.lpSum(x[n][W-2] for n in range(N)) == 1  # Change W-1 to W-2 as indices start from 0

# Flow conservation
for n in range(N):
    for w in range(1, W):  # for w = 1 to W-1
        problem += x[n][w-1] - x[n][w] + (y[n-1][w] if n > 0 else 0) - y[n][w] == 0 

# Solve the problem
problem.solve()

# Output results
paths = [(n+1, w+1) for n in range(N) for w in range(W-1) if pulp.value(x[n][w]) == 1] + \
        [(n+1, w+1) for n in range(N-1) for w in range(W) if pulp.value(y[n][w]) == 1]

total_time = pulp.value(problem.objective)
print(f'Paths: {paths}')
print(f'Total Time: {total_time}')
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')