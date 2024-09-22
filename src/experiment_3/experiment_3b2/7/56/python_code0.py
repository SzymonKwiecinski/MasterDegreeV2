import pulp
import json

# Input data
data = json.loads("{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}")

# Extract parameters from data
west_time = data['west_time']
north_time = data['north_time']
N = len(west_time)  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues (west_time has W-1 columns)

# Create the problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Decision Variables
x_west = pulp.LpVariable.dicts("x_west", (range(1, N + 1), range(1, W)), cat='Binary')
x_north = pulp.LpVariable.dicts("x_north", (range(1, N), range(1, W + 1)), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * x_west[n][w] for n in range(1, N + 1) for w in range(1, W)) +
    pulp.lpSum(north_time[n-1][w-1] * x_north[n][w] for n in range(1, N) for w in range(1, W + 1))
)

# Constraints
# Start at (1, 1)
problem += (pulp.lpSum(x_west[1][w] for w in range(2, W + 1)) + pulp.lpSum(x_north[n][1] for n in range(2, N + 1)) == 1)

# Reach (N, W)
problem += (pulp.lpSum(x_west[N][w] for w in range(1, W)) + pulp.lpSum(x_north[n][W] for n in range(1, N)) == 1)

# Flow conservation for 2 <= n <= N-1 and 2 <= w <= W-1
for n in range(2, N):
    for w in range(2, W):
        problem += (
            pulp.lpSum(x_west[n][w_prime] for w_prime in range(1, w)) + 
            pulp.lpSum(x_north[n_prime][w] for n_prime in range(1, n)) ==
            pulp.lpSum(x_west[n][w_prime] for w_prime in range(w + 1, W + 1)) + 
            pulp.lpSum(x_north[n_prime][w] for n_prime in range(n + 1, N + 1))
        )

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')