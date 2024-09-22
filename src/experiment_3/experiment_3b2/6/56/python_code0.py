import pulp
import json

# Data extraction from JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1  # rows
W = len(west_time[0]) + 1  # columns

# Define the problem
problem = pulp.LpProblem("Minimize_Time", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w, direction) 
                                  for n in range(1, N + 1) 
                                  for w in range(1, W + 1) 
                                  for direction in ['west', 'north']), 
                           cat='Binary')

# Objective function
problem += (
    pulp.lpSum(x[n][w]['west'] * west_time[n-1][w-1] for n in range(1, N + 1) for w in range(1, W)) +
    pulp.lpSum(x[n][w]['north'] * north_time[n-1][w-1] for n in range(1, N) for w in range(1, W + 1))
)

# Constraints
# Constraint 1
for n in range(2, N):
    for w in range(2, W):
        problem += (
            x[n][w - 1]['west'] + x[n - 1][w]['north'] == 
            x[n][w]['west'] + x[n][w]['north']
        )

# Constraint 2
problem += x[1][1]['west'] + x[1][1]['north'] == 1

# Constraint 3
problem += x[N][W - 1]['west'] + x[N - 1][W]['north'] == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')