import pulp

# Parse the input data
data = {
    "west_time": [[3.5, 4.5], [4, 4], [5, 4]], 
    "north_time": [[10, 10, 9], [9, 9, 12]]
}

west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1
W = len(west_time[0]) + 1

# Problem Definition
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    north_time[n][w] * x[n+1, w] + west_time[n][w] * x[n, w+1]
    for n in range(N-1) for w in range(W-1)
)

# Constraints
problem += x[0, 0] == 1, "Start at (1,1)"
problem += x[N-1, W-1] == 1, "End at (N,W)"

for n in range(N):
    for w in range(W):
        # Flow conservation constraints
        if n < N-1:
            problem += (x[n, w] >= x[n+1, w], f"North_flow_conserv_{n}_{w}")
        if w < W-1:
            problem += (x[n, w] >= x[n, w+1], f"West_flow_conserv_{n}_{w}")

# Solve the problem
problem.solve()

# Extracting Output
paths = [(n+1, w+1) for n in range(N) for w in range(W) if pulp.value(x[n, w]) == 1]
total_time = pulp.value(problem.objective)

output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')