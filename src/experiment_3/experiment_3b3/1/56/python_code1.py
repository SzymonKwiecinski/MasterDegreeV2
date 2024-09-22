import pulp

# Data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

# Dimensions
N = len(north_time) + 1
W = len(west_time[0]) + 1

# Initialize problem
problem = pulp.LpProblem("Optimal_Delivery_Path", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective Function
problem += pulp.lpSum(north_time[n-1][w-1] * x[(n, w)] for n in range(1, N) for w in range(1, W)) + \
           pulp.lpSum(west_time[n-1][w-1] * y[(n, w)] for n in range(1, N) for w in range(1, W))

# Constraints

# Movement constraints
for n in range(1, N):
    for w in range(1, W):
        problem += x[(n, w)] + y[(n, w)] == 1

# Start and end constraints
problem += x[(1, 1)] + y[(1, 1)] == 1
problem += x[(N-1, W-1)] + y[(N-1, W)] == 1

# Total number of moves
problem += pulp.lpSum(x[(n, w)] for n in range(1, N) for w in range(1, W)) == N-1
problem += pulp.lpSum(y[(n, w)] for n in range(1, N) for w in range(1, W)) == W-1

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')