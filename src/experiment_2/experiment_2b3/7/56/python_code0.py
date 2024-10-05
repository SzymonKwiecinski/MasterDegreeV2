import pulp

# Parse the input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract grid dimensions
west_time = data['west_time']
north_time = data['north_time']
N = len(west_time)
W = len(west_time[0]) + 1

# Initialize the problem
problem = pulp.LpProblem("Optimal_Delivery_Path", pulp.LpMinimize)

# Variables: x_n_w: flow through the path at (n, w)
x_vars = {(n, w): pulp.LpVariable(f"x_{n}_{w}", cat="Binary") for n in range(N) for w in range(W)}

# Objective function: Minimize total travel time
problem += pulp.lpSum([
    west_time[n][w] * x_vars[n, w+1] + north_time[n][w] * x_vars[n+1, w]
    for n in range(N) for w in range(W - 1)
    if n < N-1 and w < W
]), "Total_Travel_Time"

# Constraint: Start at (0, 0)
problem += x_vars[0, 0] == 1, "Start_Constraint"

# Constraint: End at (N-1, W-1)
problem += x_vars[N-1, W-1] == 1, "End_Constraint"

# Constraints: Flow conservation
for n in range(N):
    for w in range(W):
        if n == 0 and w == 0:
            continue
        elif n == N-1 and w == W-1:
            continue
        in_flow = (x_vars[n-1, w] if n > 0 else 0) + (x_vars[n, w-1] if w > 0 else 0)
        out_flow = (x_vars[n+1, w] if n < N-1 else 0) + (x_vars[n, w+1] if w < W-1 else 0)
        problem += in_flow == out_flow, f"Flow_Conservation_{n}_{w}"

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Extract the paths
paths = [(n, w) for n in range(N) for w in range(W) if pulp.value(x_vars[n, w]) > 0.5]

# Calculate the total time
total_time = sum(
    west_time[n][w] * pulp.value(x_vars[n, w+1]) + north_time[n][w] * pulp.value(x_vars[n+1, w])
    for n in range(N) for w in range(W - 1)
    if n < N-1 and w < W
)

# Output result
result = {
    "paths": paths,
    "total_time": total_time
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')