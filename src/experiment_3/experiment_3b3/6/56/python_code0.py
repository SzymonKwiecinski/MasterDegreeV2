import pulp

# Data from the problem
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Determine the grid size based on data dimensions
N = len(data['north_time']) + 1
W = len(data['west_time'][0]) + 1

# Initialize the problem
problem = pulp.LpProblem("Delivery Path Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N-1) for w in range(W-1)), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(N-1) for w in range(W-1)), cat='Binary')

# Objective function: Minimize total time
problem += pulp.lpSum(x[n, w] * data['north_time'][n][w] + y[n, w] * data['west_time'][n][w] 
                      for n in range(N-1) for w in range(W-1))

# Constraint 1: Total moves
m = (N - 1) + (W - 1)  # since to reach end need N-1 north and W-1 west moves
problem += (pulp.lpSum(x[N-2, w] for w in range(W-1)) + 
            pulp.lpSum(y[n, W-2] for n in range(N-1)) == m)

# Constraint 2: Flow conservation
for n in range(N-1):
    for w in range(W-1):
        problem += (x[n, w] + y[n, w] == 1)

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')