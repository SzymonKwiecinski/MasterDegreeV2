import pulp

# Data
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

# Nodes and links
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']

# Problem initialization
problem = pulp.LpProblem("CommunicationNetwork", pulp.LpMinimize)

# Decision variables
x = {}
links = zip(start_nodes, end_nodes)
for (i, j), capacity in zip(links, capacities):
    x[(i, j)] = pulp.LpVariable(f"x_{i}_{j}", lowBound=0, upBound=capacity, cat='Continuous')

# Objective function
problem += pulp.lpSum(costs[idx] * x[(start_nodes[idx], end_nodes[idx])] for idx in range(data['NumLinks']))

# Capacity constraints
for idx, (i, j) in enumerate(zip(start_nodes, end_nodes)):
    problem += x[(i, j)] <= capacities[idx]

# Flow conservation constraints
flow_requirements = zip(data['Source'], data['Destination'], data['DataRate'])
nodes = set(start_nodes) | set(end_nodes)

for k in nodes:
    for source, destination, data_rate in flow_requirements:
        incoming_flow = pulp.lpSum(x[(i, k)] for i in start_nodes if (i, k) in x)
        outgoing_flow = pulp.lpSum(x[(k, j)] for j in end_nodes if (k, j) in x)
        if k == source:
            problem += outgoing_flow - incoming_flow == data_rate
        elif k == destination:
            problem += outgoing_flow - incoming_flow == -data_rate
        else:
            problem += outgoing_flow - incoming_flow == 0

# Solve the problem
problem.solve()

# Output the results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

# Find optimized paths
for source, destination, data_rate in flow_requirements:
    path_flow = 0
    path_cost = 0
    route = [source]
    current_node = source

    while current_node != destination:
        for (i, j) in x:
            if i == current_node and x[(i, j)].varValue > 0:
                path_flow = x[(i, j)].varValue
                path_cost += path_flow * costs[start_nodes.index(i)]
                route.append(j)
                current_node = j
                break

    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

print(optimized_paths)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")