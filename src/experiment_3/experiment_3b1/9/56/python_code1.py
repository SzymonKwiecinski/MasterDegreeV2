import pulp
import json

# Load data from JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')

# Define parameters
west_time = data['west_time']
north_time = data['north_time']
N = len(north_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Create the problem instance
problem = pulp.LpProblem("Delivery_Path_Optimization", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N+1) for w in range(1, W+1)), cat='Binary')

# Objective function
problem += pulp.lpSum(west_time[n-1][w-1] * x[n][w] for n in range(1, N) for w in range(1, W+1)) + \
            pulp.lpSum(north_time[n-1][w-1] * x[n][w] for n in range(1, N) for w in range(1, W+1))

# Constraints
# Flow Conservation
for n in range(1, N+1):
    for w in range(1, W+1):
        problem += pulp.lpSum(x[n][w_prime] for w_prime in range(1, W+1)) + pulp.lpSum(x[n_prime][w] for n_prime in range(1, N+1)) == 1

# Starting Point
problem += x[1][1] == 1

# Ending Point
problem += x[N][W] == 1

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')