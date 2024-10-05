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

# Unpack data
num_links = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
num_flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Initialize the problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Flow", [(i, j) for i, j in zip(start_nodes, end_nodes)], lowBound=0)

# Objective function
problem += pulp.lpSum([costs[idx] * x[(start_nodes[idx], end_nodes[idx])] for idx in range(num_links)])

# Constraints
# Capacity constraints
for idx in range(num_links):
    problem += x[(start_nodes[idx], end_nodes[idx])] <= capacities[idx]

# Flow conservation constraints
all_nodes = set(start_nodes).union(set(end_nodes))
intermediate_nodes = all_nodes.difference(set(sources + destinations))

for k in intermediate_nodes:
    inflow = pulp.lpSum([x[(i, k)] for i in start_nodes if (i, k) in x])
    outflow = pulp.lpSum([x[(k, j)] for j in end_nodes if (k, j) in x])
    problem += inflow == outflow

# Supply constraints for source nodes
for idx, (source, dest) in enumerate(zip(sources, destinations)):
    outflow = pulp.lpSum([x[(source, j)] for j in end_nodes if (source, j) in x])
    problem += outflow == data_rates[idx]

# Demand constraints for destination nodes
for destination in destinations:
    inflow = pulp.lpSum([x[(i, destination)] for i in start_nodes if (i, destination) in x])
    total_data_rate_to_destination = sum(data_rates[idx] for idx, dest in enumerate(destinations) if dest == destination)
    problem += inflow == total_data_rate_to_destination

# Solve the problem
problem.solve()

# Prepare output
optimized_paths = []
for idx in range(num_flow_reqs):
    source = sources[idx]
    destination = destinations[idx]
    path_flow = 0
    path_cost = 0
    current_node = source
    route = [current_node]

    while current_node != destination:
        for next_node in end_nodes:
            if (current_node, next_node) in x and pulp.value(x[(current_node, next_node)]) > 0:
                path_flow = pulp.value(x[(current_node, next_node)])
                path_cost += costs[start_nodes.index(current_node)] * path_flow
                current_node = next_node
                route.append(current_node)
                break
    
    optimized_paths.append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

total_cost = pulp.value(problem.objective)

# Output JSON
output_data = {
    "optimized_paths": {
        "paths": optimized_paths,
        "total_cost": total_cost
    }
}

import json
print(json.dumps(output_data, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')