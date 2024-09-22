import pulp
import json

# Input data
data = '{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}'
data_dict = json.loads(data)

# Define dimensions
N = len(data_dict['north_time']) + 1  # +1 for the additional row (1-based index)
W = len(data_dict['north_time'][0]) + 1  # +1 for the additional column (1-based index)

# Create the problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Decision Variables
x_N = pulp.LpVariable.dicts("North", ((n, w) for n in range(1, N + 1) for w in range(1, W + 1)), cat='Binary')
x_W = pulp.LpVariable.dicts("West", ((n, w) for n in range(1, N + 1) for w in range(1, W + 1)), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(data_dict['west_time'][n-1][w-1] * x_W[n, w] for n in range(1, N + 1) for w in range(1, W)) +
    pulp.lpSum(data_dict['north_time'][n-1][w-1] * x_N[n, w] for n in range(1, N) for w in range(1, W + 1))
)

# Constraints

# Starting point constraint
problem += x_N[1, 1] + x_W[1, 1] == 1

# Flow conservation constraints
for n in range(1, N + 1):
    for w in range(1, W + 1):
        if not (n == 1 and w == 1):
            if n > 1 and w > 1:
                problem += (x_N[n, w] + x_W[n, w]) - (x_N[n - 1, w] + x_W[n, w - 1]) == 0
            elif n > 1:
                problem += x_N[n, w] - x_N[n - 1, w] == 0
            elif w > 1:
                problem += x_W[n, w] - x_W[n, w - 1] == 0

# Destination point constraint
problem += x_W[N, W - 1] + x_N[N - 1, W] == 1

# Solve the problem
problem.solve()

# Print out the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')