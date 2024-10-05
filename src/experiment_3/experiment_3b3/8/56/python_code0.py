import pulp

# Data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

# Problem dimensions
N = len(north_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Initialize the problem
problem = pulp.LpProblem("Delivery_Problem", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", [(n, w) for n in range(1, N) for w in range(1, W)], cat='Binary')
y = pulp.LpVariable.dicts("y", [(n, w) for n in range(1, N) for w in range(1, W)], cat='Binary')

# Objective function
problem += (
    pulp.lpSum(north_time[n-1][w-1] * x[n, w] for n in range(1, N) for w in range(1, W)) +
    pulp.lpSum(west_time[n-1][w-1] * y[n, w] for n in range(1, N) for w in range(1, W-1))
)

# Constraints
# Movement constraints
for n in range(1, N):
    for w in range(1, W):
        problem += x[n, w] + y[n, w] <= 1

# Boundary conditions for the beginning of the path
problem += pulp.lpSum(y[1, w] for w in range(1, W-1)) == 0

# Boundary conditions for the end of the path
problem += pulp.lpSum(x[N-1, w] for w in range(1, W)) == 1

# Solve the problem
problem.solve()

# Extract the results
total_time = pulp.value(problem.objective)
paths = []
for n in range(1, N):
    for w in range(1, W):
        if pulp.value(x[n, w]) == 1:
            paths.append(f"Move North from ({w}, {n})")
        elif pulp.value(y[n, w]) == 1:
            paths.append(f"Move West from ({w}, {n})")

# Output the results
print(f'Paths: {paths}')
print(f'Total Time: {total_time}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')