import pulp
import json

data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract data
west_time = data['west_time']
north_time = data['north_time']
N = len(west_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Create the problem
problem = pulp.LpProblem("DeliveryTimeOptimization", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum(west_time[n-1][w-1] * x[n, w] + north_time[n-1][w-1] * x[n, w] for n in range(1, N) for w in range(1, W-1))

# Constraints
# 1. Must arrive at the destination
problem += pulp.lpSum(x[N-1, w] for w in range(1, W)) == 1

# 2. Each intersection can only be entered from the west or north
for n in range(1, N):
    problem += pulp.lpSum(x[n, w] for w in range(1, W)) <= 1  # Constraint (2)
for w in range(1, W):
    problem += pulp.lpSum(x[n, w] for n in range(1, N)) <= 1  # Constraint (3)

# Solve the problem
problem.solve()

# Output results
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[n, w]) == 1]

print(f'Paths: {paths}')
print(f'Total Time: <OBJ>{pulp.value(problem.objective)}</OBJ>')