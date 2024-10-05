import pulp

# Data input
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extract west_time and north_time
west_time = data['west_time']
north_time = data['north_time']

# Determine grid size
N = len(north_time) + 1  # number of streets
W = len(west_time[0]) + 1  # number of avenues

# Initialize the model
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

# Variables for flow on each path
flow_vars = {}
for n in range(N):
    for w in range(W):
        if n < N - 1:
            flow_vars[(n, w, 'N')] = pulp.LpVariable(f"flow_N_{n}_{w}", cat=pulp.LpBinary)
        if w < W - 1:
            flow_vars[(n, w, 'W')] = pulp.LpVariable(f"flow_W_{n}_{w}", cat=pulp.LpBinary)

# Objective function: Minimize total travel time
problem += (
    pulp.lpSum(north_time[n][w] * flow_vars[(n, w, 'N')] for n in range(N - 1) for w in range(W)) +
    pulp.lpSum(west_time[n][w] * flow_vars[(n, w, 'W')] for n in range(N) for w in range(W - 1))
)

# Constraints
# Starting point
problem += pulp.lpSum(flow_vars[(0, 0, d)] for d in ['N', 'W']) == 1

# Ending point
problem += pulp.lpSum(flow_vars[(N - 1, W - 1, 'N')]) == 0
problem += pulp.lpSum(flow_vars[(N - 1, W - 1, 'W')]) == 0

# Flow continuity
for n in range(N):
    for w in range(W):
        in_flow = []
        out_flow = []
        if n > 0:
            in_flow.append(flow_vars[(n - 1, w, 'N')])
        if w > 0:
            in_flow.append(flow_vars[(n, w - 1, 'W')])
        if n < N - 1:
            out_flow.append(flow_vars[(n, w, 'N')])
        if w < W - 1:
            out_flow.append(flow_vars[(n, w, 'W')])
        
        if in_flow or out_flow:
            problem += (
                pulp.lpSum(in_flow) - pulp.lpSum(out_flow) == (1 if (n, w) == (0, 0) else 0)
            )

# Solve the problem
problem.solve()

# Extracting the paths
paths = []
for n in range(N):
    for w in range(W):
        if n < N - 1 and pulp.value(flow_vars[(n, w, 'N')]) > 0.5:
            paths.append((n + 1, w))
        if w < W - 1 and pulp.value(flow_vars[(n, w, 'W')]) > 0.5:
            paths.append((n, w + 1))

# Calculating total travel time
total_time = pulp.value(problem.objective)

# Output format
solution = {
    "paths": paths,
    "total_time": total_time
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')