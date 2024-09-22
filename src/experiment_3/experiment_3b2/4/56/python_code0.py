import pulp
import json

# Data
data = json.loads("{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}")
west_time = data['west_time']
north_time = data['north_time']

N = len(west_time)    # Number of rows
W = len(west_time[0]) # Number of columns for west_time (assuming it's rectangular)

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_time", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", ((n, w, d) for n in range(1, N+1) for w in range(1, W+1) for d in ['W', 'N']), lowBound=0, upBound=1, cat='Binary')

# Objective Function
problem += pulp.lpSum(west_time[n-1][w-1] * x[(n, w, 'W')] for n in range(1, N+1) for w in range(1, W)) + \
            pulp.lpSum(north_time[n-1][w-1] * x[(n, w, 'N')] for n in range(1, N) for w in range(1, W+1))

# Constraints
problem += x[(1, 1, 'W')] + x[(1, 1, 'N')] == 1
problem += x[(N, W-1, 'W')] + x[(N-1, W, 'N')] == 1

for n in range(2, N+1):
    for w in range(2, W+1):
        problem += (x[(n, w-1, 'W')] + x[(n-1, w, 'N')] == x[(n, w, 'W')] + x[(n, w, 'N')])

for n in range(1, N):
    for w in range(1, W):
        problem += (x[(n, w, 'W')] + x[(n, w, 'N')] <= 1)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')