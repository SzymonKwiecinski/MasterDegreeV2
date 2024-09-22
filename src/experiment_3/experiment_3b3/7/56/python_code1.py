import pulp

# Problem data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Dimensions of the grid
N = len(data['north_time']) + 1  # Number of streets
W = len(data['west_time'][0]) + 1  # Number of avenues

# Create a linear programming problem
problem = pulp.LpProblem("Path_Optimization", pulp.LpMinimize)

# Decision variables
x_vars = pulp.LpVariable.dicts("X", [(n, w) for n in range(1, N) for w in range(1, W)], 
                               cat='Binary')
y_vars = pulp.LpVariable.dicts("Y", [(n, w) for n in range(1, N) for w in range(1, W)], 
                               cat='Binary')

# Objective function
problem += pulp.lpSum(data['north_time'][n-1][w-1] * x_vars[(n, w)] for n in range(1, N) for w in range(1, W-1)) + \
           pulp.lpSum(data['west_time'][n-1][w-1] * y_vars[(n, w)] for n in range(1, N) for w in range(1, W-1))

# Constraints

# Every intersection must have at most one move
for n in range(1, N):
    for w in range(1, W):
        problem += x_vars[(n, w)] + y_vars[(n, w)] <= 1

# Flow conservation constraints
for n in range(1, N-1):
    for w in range(1, W-1):
        problem += pulp.lpSum(x_vars[(n, k)] for k in range(1, W-1)) + pulp.lpSum(y_vars[(k, w)] for k in range(1, N-1)) == 1

# Starting condition
problem += pulp.lpSum(y_vars[(1, w)] for w in range(1, W)) == 1

# Ending condition
problem += pulp.lpSum(x_vars[(n, W-1)] for n in range(1, N)) == 1

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')