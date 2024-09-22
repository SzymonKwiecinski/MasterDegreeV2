import pulp

# Parse the input data
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

# Define nodes, links, and requirements
nodes = list(set(data['StartNode'] + data['EndNode']))
links = list(zip(data['StartNode'], data['EndNode']))
capacities = dict(zip(links, data['Capacity']))
costs = dict(zip(links, data['Cost']))
flow_requests = list(zip(data['Source'], data['Destination'], data['DataRate']))

# Create the LP problem
problem = pulp.LpProblem("Network_Flow_Optimization", pulp.LpMinimize)

# Create decision variables for flow through each link for each data request
flow_vars = {}
for idx, (k, l, b) in enumerate(flow_requests):
    for (i, j) in links:
        flow_vars[(k, l, i, j)] = pulp.LpVariable(f"flow_{k}_{l}_{i}_{j}", lowBound=0, upBound=capacities[(i, j)])

# Objective function: Minimize the total cost of transmitting data
problem += pulp.lpSum(flow_vars[(k, l, i, j)] * costs[(i, j)] for (k, l, _b) in flow_requests for (i, j) in links)

# Constraints to ensure flow conservation
for (k, l, b) in flow_requests:
    for node in nodes:
        flow_in = pulp.lpSum(flow_vars[(k, l, i, node)] for (i, node) in links if i != node)
        flow_out = pulp.lpSum(flow_vars[(k, l, node, j)] for (node, j) in links if j != node)
        if node == k:  # Source node
            problem += (flow_out - flow_in == b)
        elif node == l:  # Destination node
            problem += (flow_in - flow_out == b)
        else:
            problem += (flow_in == flow_out)

# Solve the problem
problem.solve()

# Gather the results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

# Extract paths and costs
for (k, l, _b) in flow_requests:
    path_flow = 0
    path_cost = 0
    route = []
    
    for (i, j) in links:
        if pulp.value(flow_vars[(k, l, i, j)]) > 0:
            path_flow += pulp.value(flow_vars[(k, l, i, j)])
            path_cost += pulp.value(flow_vars[(k, l, i, j)]) * costs[(i, j)]
            route.extend([i, j])
    
    if route:
        optimized_paths["paths"].append({
            "source": k,
            "destination": l,
            "route": list(dict.fromkeys(route)),  # Remove duplicates in path
            "path_flow": path_flow,
            "path_cost": path_cost
        })

print(f'Optimized paths and costs: {optimized_paths}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')