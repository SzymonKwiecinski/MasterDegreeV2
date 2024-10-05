import pulp

# Data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

west_time = data['west_time']
north_time = data['north_time']

W = len(west_time[0]) + 1  # Number of avenues
N = len(north_time) + 1    # Number of streets

# Problem
problem = pulp.LpProblem("DeliveryPathProblem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum([north_time[n-1][w-1] * x[n, w] + west_time[n-1][w-1] * x[n, w] for n in range(1, N) for w in range(1, W)])

# Constraints
# Start at (1,1)
problem += (pulp.lpSum([x[1, w] for w in range(1, W)]) + pulp.lpSum([x[n, 1] for n in range(1, N)]) == 1)

# End at (W,N)
problem += (pulp.lpSum([x[N-1, w] for w in range(1, W)]) + pulp.lpSum([x[n, W-1] for n in range(1, N)]) == 1)

# Solve the problem
problem.solve()

# Output the results
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[n, w]) == 1]
total_time = pulp.value(problem.objective)

output = {
    "paths": paths,
    "total_time": total_time
}

print(output)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')