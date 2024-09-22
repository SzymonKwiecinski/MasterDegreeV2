import pulp
import json

# Load data from JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

# Define dimensions
N = len(north_time) + 1  # Number of streets (including starting street)
W = len(west_time[0]) + 1  # Number of avenues (including starting avenue)

# Define the problem
problem = pulp.LpProblem("DeliveryPath", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N-1) for w in range(W)), cat='Binary')  # moving north
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(N) for w in range(W-1)), cat='Binary')  # moving west

# Objective function
problem += pulp.lpSum(north_time[n][w] * x[n, w] for n in range(N-1) for w in range(W)) + \
            pulp.lpSum(west_time[n][w] * y[n, w] for n in range(N) for w in range(W-1)), "TotalTravelTime"

# Flow constraints
for n in range(N):
    problem += pulp.lpSum(y[n, w] for w in range(W-1)) + pulp.lpSum(x[n-1, w] for w in range(W) if n > 0) == 1, f"FlowConstraint_n{n}"

# Solve the problem
problem.solve()

# Output results
paths = []
for n in range(N-1):
    for w in range(W):
        if pulp.value(x[n, w]) == 1:
            paths.append((n + 1, w))  # Store path given street n+1 and avenue w
for n in range(N):
    for w in range(W-1):
        if pulp.value(y[n, w]) == 1:
            paths.append((n + 1, w + 1))  # Store path given street n+1 and avenue w+1

total_time = pulp.value(problem.objective)
print(f'Paths Taken: {paths}')
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')