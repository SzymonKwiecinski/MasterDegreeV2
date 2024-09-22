import pulp
import json

# Load data
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

# Define the number of streets and avenues
N = len(north_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Create the linear programming problem
problem = pulp.LpProblem("DeliveryPath", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum(x[n, w] * west_time[n-1][w-1] + y[n, w] * north_time[n-1][w-1] for n in range(1, N) for w in range(1, W))

# Constraints
# Start at (1,1)
problem += pulp.lpSum(x[1, w] for w in range(1, W)) + pulp.lpSum(y[n, 1] for n in range(1, N)) == 1

# End at (W,N)
problem += pulp.lpSum(y[n, W-1] for n in range(1, N)) + pulp.lpSum(x[N-1, w] for w in range(1, W)) == 1

# Intermediate intersections
for n in range(1, N):
    for w in range(1, W):
        problem += pulp.lpSum(x[n, w] for n in range(1, N)) + pulp.lpSum(y[n, w] for n in range(1, N)) == \
                   pulp.lpSum(y[n, w+1] for n in range(1, N)) + pulp.lpSum(x[n+1, w] for n in range(1, N))

# Solve the problem
problem.solve()

# Collect the paths taken
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[n, w]) == 1 or pulp.value(y[n, w]) == 1]
total_time = pulp.value(problem.objective)

# Print the result
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')