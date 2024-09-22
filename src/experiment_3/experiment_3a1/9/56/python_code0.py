import pulp
import json

# Data in JSON format as a python dictionary
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 
        'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting parameters from the data
west_time = data['west_time']
north_time = data['north_time']
N = len(north_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Create a linear programming problem
problem = pulp.LpProblem("Delivery_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), 0, 1, pulp.LpBinary)
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N) for w in range(1, W)), 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum(north_time[n-1][w-1] * x[n, w] + west_time[n-1][w-1] * y[n, w]
                       for n in range(1, N) for w in range(1, W))

# Constraints
# Starting point movement constraints
problem += pulp.lpSum(y[1, w] for w in range(1, W)) == 1  # Start moving east from (1,1)
problem += pulp.lpSum(x[n, 1] for n in range(1, N)) == 1  # Start moving north from (1,1)

# Flow conservation constraints
for n in range(1, N):
    problem += (pulp.lpSum(y[n, w] for w in range(1, W)) ==
                pulp.lpSum(x[n, w-1] for w in range(1, W)))

for w in range(1, W):
    problem += (pulp.lpSum(x[n, w] for n in range(1, N)) ==
                pulp.lpSum(y[n-1, w] for n in range(1, N)))

# Solve the problem
problem.solve()

# Output the paths and total time
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[n, w]) == 1 or pulp.value(y[n, w]) == 1]
total_time = pulp.value(problem.objective)

print(f'Paths: {paths}')
print(f'Total Time: {total_time}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')