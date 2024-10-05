import pulp

# Data from JSON
data = {
    'NumLinks': 4,
    'StartNode': [1, 2, 2, 3],
    'EndNode': [2, 3, 4, 4],
    'Capacity': [50, 40, 60, 50],
    'Cost': [2, 3, 1, 1],
    'NumFlowReqs': 2,
    'Source': [1, 2],
    'Destination': [4, 3],
    'DataRate': [40, 30]
}

# Initialize problem
problem = pulp.LpProblem("Network_Flow_Min_Cost", pulp.LpMinimize)

# Variables for flow along each link
flow_vars = {}
for idx in range(data['NumLinks']):
    start, end = data['StartNode'][idx], data['EndNode'][idx]
    flow_vars[(start, end)] = pulp.LpVariable(f'flow_{start}_{end}', lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(start, end)] * data['Cost'][idx] for idx, (start, end) in enumerate(zip(data['StartNode'], data['EndNode'])))

# Capacity constraints for each link
for idx in range(data['NumLinks']):
    start, end = data['StartNode'][idx], data['EndNode'][idx]
    problem += flow_vars[(start, end)] <= data['Capacity'][idx], f"Cap_Constr_{start}_{end}"

# Flow conservation constraints and data rate requirements
for req_idx in range(data['NumFlowReqs']):
    source, destination = data['Source'][req_idx], data['Destination'][req_idx]
    rate = data['DataRate'][req_idx]

    # Source constraint
    problem += pulp.lpSum(flow_vars[(node, destination)] for node in data['StartNode'] if (node, destination) in flow_vars) - pulp.lpSum(flow_vars[(source, node)] for node in data['EndNode'] if (source, node) in flow_vars) == -rate, f"Source_Constr_{source}_{destination}"

    # Sink constraint
    problem += pulp.lpSum(flow_vars[(source, node)] for node in data['EndNode'] if (source, node) in flow_vars) - pulp.lpSum(flow_vars[(node, source)] for node in data['StartNode'] if (node, source) in flow_vars) == rate, f"Sink_Constr_{source}_{destination}"

# Solve the problem
problem.solve()

# Extracting results
optimized_paths = []
total_cost = pulp.value(problem.objective)

for req_idx in range(data['NumFlowReqs']):
    source, destination = data['Source'][req_idx], data['Destination'][req_idx]
    path_flow = sum(flow_vars[(start, end)].varValue for start, end in flow_vars if start == source and end == destination)
    path_cost = sum(flow_vars[(start, end)].varValue * data['Cost'][data['StartNode'].index(start)] for start, end in flow_vars if start == source and end == destination)
    optimized_paths.append({
        "source": source,
        "destination": destination,
        "route": [source, destination],  # Assuming direct path for simplicity
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output result
output = {
    "optimized_paths": {
        "paths": optimized_paths,
        "total_cost": total_cost
    }
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')