import pulp

# Problem Definition
problem = pulp.LpProblem("Delivery_Path_Optimization", pulp.LpMinimize)

# Data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

# Grid dimensions
N = len(north_time) + 1
W = len(west_time[0]) + 1

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N) for w in range(1, W)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(x[n, w] + y[n, w] for n in range(1, N) for w in range(1, W)), "Total Walking Time"

# Flow Constraints
for n in range(1, N):
    for w in range(1, W):
        if w < W - 1:
            problem += x[n, w] == west_time[n-1][w-1]
        if n < N - 1:
            problem += y[n, w] == north_time[n-1][w-1]

# Solve
problem.solve()

# Output
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[n, w]) > 0 or pulp.value(y[n, w]) > 0]
total_time = pulp.value(problem.objective)

print({
    "paths": paths,
    "total_time": total_time
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')