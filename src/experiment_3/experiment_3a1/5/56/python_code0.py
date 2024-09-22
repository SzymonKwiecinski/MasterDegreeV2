import pulp
import json

# Load the data
data_json = '''{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}'''
data = json.loads(data_json.replace("'", '"'))

west_time = data['west_time']
north_time = data['north_time']
N = len(north_time) + 1  # Number of rows (intersections)
W = len(west_time[0]) + 1  # Number of columns (intersections)

# Define the problem
problem = pulp.LpProblem("Delivery_Person_Optimal_Path", pulp.LpMinimize)

# Define variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Define the objective function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * x[n, w] for n in range(1, N) for w in range(1, W)) +
    pulp.lpSum(north_time[n-1][w-1] * y[n, w] for n in range(1, N) for w in range(1, W))
)

# Add flow conservation constraints for moving west
for w in range(1, W):
    problem += (pulp.lpSum(x[n, w] for n in range(1, N)) == 
                 pulp.lpSum(y[n, w] for n in range(1, N)) + 1)

# Add flow conservation constraints for moving north
for n in range(1, N):
    problem += (pulp.lpSum(y[n, w] for w in range(1, W)) == 
                 pulp.lpSum(x[n, w] for w in range(1, W)) + 1)

# Solve the problem
problem.solve()

# Extract the paths
paths = []
for w in range(1, W):
    for n in range(1, N):
        if pulp.value(x[n, w]) == 1:
            paths.append((n, w))
        if pulp.value(y[n, w]) == 1:
            paths.append((n, w))

# Print the total time and objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')