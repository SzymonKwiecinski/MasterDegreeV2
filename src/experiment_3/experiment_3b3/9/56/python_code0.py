import pulp

data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1
W = len(west_time[0]) + 1

# Define the problem
problem = pulp.LpProblem("Delivery_Person_Path_Optimization", pulp.LpMinimize)

# Define variables
x = pulp.LpVariable.dicts("x", [(n, w) for n in range(1, N) for w in range(1, W)], cat='Binary')
y = pulp.LpVariable.dicts("y", [(n, w) for n in range(1, N) for w in range(1, W)], cat='Binary')

# Objective Function
problem += pulp.lpSum([west_time[n-1][w-1] * x[n,w] for n in range(1, N) for w in range(1, W)]) + \
           pulp.lpSum([north_time[n-1][w-1] * y[n,w] for n in range(1, N) for w in range(1, W)])

# Constraints
for n in range(1, N):
    problem += pulp.lpSum([x[n, w] for w in range(1, W)]) <= 1

for w in range(1, W):
    problem += pulp.lpSum([y[n, w] for n in range(1, N)]) <= 1

problem += x[1, 1] + y[1, 1] == 1
problem += x[N-1, W-1] + y[N-1, W-1] == 0

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Extract the optimal path
path = []
for n in range(1, N):
    for w in range(1, W):
        if pulp.value(x[n, w]) == 1.0:
            path.append((n, w))
        if pulp.value(y[n, w]) == 1.0:
            path.append((n, w))

print("Paths:", path)