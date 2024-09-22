import pulp

# Define data from JSON
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

# Problem definition
problem = pulp.LpProblem("NetworkFlowOptimization", pulp.LpMinimize)

# Variables
flow_vars = {}
for i in range(data['NumLinks']):
    flow_vars[i] = pulp.LpVariable(f'flow_{i}', lowBound=0, upBound=data['Capacity'][i], cat=pulp.LpContinuous)

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[i] * data['Cost'][i] for i in range(data['NumLinks']))

# Constraints

# Flow conservation constraints for each node
nodes = set(data['StartNode'] + data['EndNode'])
flow_reqs = list(zip(data['Source'], data['Destination'], data['DataRate']))

for k in range(data['NumFlowReqs']):
    source = data['Source'][k]
    destination = data['Destination'][k]
    rate = data['DataRate'][k]

    for node in nodes:
        if node == source:
            problem += pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['StartNode'][i] == node) \
                       - pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['EndNode'][i] == node) == rate
        elif node == destination:
            problem += pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['EndNode'][i] == node) \
                       - pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['StartNode'][i] == node) == rate
        else:
            problem += pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['StartNode'][i] == node) \
                       - pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['EndNode'][i] == node) == 0

# Solve the problem
problem.solve()

# Result extraction
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for flow_id in range(data['NumFlowReqs']):
    source = data['Source'][flow_id]
    destination = data['Destination'][flow_id]
    rate = data['DataRate'][flow_id]
    path_flow = 0
    path_cost = 0
    route = []

    for i in range(data['NumLinks']):
        if pulp.value(flow_vars[i]) > 0:
            route.append(data['StartNode'][i])
            if data['EndNode'][i] == destination:
                route.append(destination)
                path_flow += pulp.value(flow_vars[i])
                path_cost += pulp.value(flow_vars[i]) * data['Cost'][i]
                break

    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": list(sorted(set(route))),
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output the result
result = optimized_paths
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')