import pulp

# Parsing input data
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

links = [{'start': data['StartNode'][i], 'end': data['EndNode'][i], 'U': data['Capacity'][i], 'C': data['Cost'][i]} for i in range(data['NumLinks'])]
flow_reqs = [{'source': data['Source'][i], 'destination': data['Destination'][i], 'rate': data['DataRate'][i]} for i in range(data['NumFlowReqs'])]

# Create a list of all nodes
nodes = set(data['StartNode'] + data['EndNode'])

# Create the LP problem
problem = pulp.LpProblem("Network Flow Optimization", pulp.LpMinimize)

# Create a dictionary of link flow variables
link_flow_vars = {(link['start'], link['end']): pulp.LpVariable(f"Flow_{link['start']}_{link['end']}", lowBound=0) for link in links}

# Objective function: Minimize total cost
problem += pulp.lpSum(link['C'] * link_flow_vars[(link['start'], link['end'])] for link in links)

# Capacity constraints for each link
for link in links:
    problem += link_flow_vars[(link['start'], link['end'])] <= link['U'], f"Cap_{link['start']}_{link['end']}"

# Flow conservation for each node and flow request
for flow in flow_reqs:
    for node in nodes:
        incoming_flow = pulp.lpSum(link_flow_vars[(start, node)] for start in nodes if (start, node) in link_flow_vars)
        outgoing_flow = pulp.lpSum(link_flow_vars[(node, end)] for end in nodes if (node, end) in link_flow_vars)
        if node == flow['source']:
            problem += (outgoing_flow - incoming_flow) == flow['rate'], f"Flow_Src_{flow['source']}_to_{flow['destination']}_at_{node}"
        elif node == flow['destination']:
            problem += (incoming_flow - outgoing_flow) == flow['rate'], f"Flow_Dest_{flow['source']}_to_{flow['destination']}_at_{node}"
        else:
            problem += (incoming_flow - outgoing_flow) == 0, f"Flow_Intermediate_Node_{node}_for_{flow['source']}_to_{flow['destination']}"

# Solve the problem
problem.solve()

# Extract results
optimized_paths = []
for flow in flow_reqs:
    source = flow['source']
    destination = flow['destination']
    path_flow = 0
    path_cost = 0
    route = [source]
    while source != destination:
        for link in links:
            if link_flow_vars[(link['start'], link['end'])].varValue > 0 and link['start'] == source:
                path_flow = link_flow_vars[(link['start'], link['end'])].varValue
                path_cost += path_flow * link['C']
                source = link['end']
                route.append(source)
                break
    optimized_paths.append({
        "source": flow['source'],
        "destination": flow['destination'],
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Print total objective/cost
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")

# Output format
output = {
    "optimized_paths": {
        "paths": optimized_paths,
        "total_cost": pulp.value(problem.objective)
    }
}

print(output)