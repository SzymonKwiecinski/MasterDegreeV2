import pulp

# Data provided in JSON format
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

# Extracting data
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Create a list of arcs (links) and their properties
arcs = [(start_node[i], end_node[i]) for i in range(num_links)]
arc_data = {(start_node[i], end_node[i]): {'U': capacity[i], 'C': cost[i]} for i in range(num_links)}

# Initialize the problem
problem = pulp.LpProblem("NetworkFlowMinCost", pulp.LpMinimize)

# Decision variables
flow = pulp.LpVariable.dicts("Flow", (range(num_flow_reqs), arcs), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(flow[f][arc] * arc_data[arc]['C'] for f in range(num_flow_reqs) for arc in arcs)

# Capacity constraints
for arc in arcs:
    problem += pulp.lpSum(flow[f][arc] for f in range(num_flow_reqs)) <= arc_data[arc]['U'], f"Cap_{arc}"

# Flow conservation constraints
for f in range(num_flow_reqs):
    for node in set(start_node + end_node):
        if node == source[f]:
            # Source node constraint
            problem += pulp.lpSum(flow[f][(node, j)] for (i, j) in arcs if i == node) - pulp.lpSum(flow[f][(i, node)] for (i, j) in arcs if j == node) == data_rate[f], f"FlowConserv_{f}_{node}"
        elif node == destination[f]:
            # Destination node constraint
            problem += pulp.lpSum(flow[f][(node, j)] for (i, j) in arcs if i == node) - pulp.lpSum(flow[f][(i, node)] for (i, j) in arcs if j == node) == -data_rate[f], f"FlowConserv_{f}_{node}"
        else:
            # Intermediate node constraint
            problem += pulp.lpSum(flow[f][(node, j)] for (i, j) in arcs if i == node) - pulp.lpSum(flow[f][(i, node)] for (i, j) in arcs if j == node) == 0, f"FlowConserv_{f}_{node}"

# Solve the problem
problem.solve()

# Prepare the output
optimized_paths = {
    "paths": []
}

for f in range(num_flow_reqs):
    path_flow = 0
    path_cost = 0
    used_arcs = [(i, j) for (i, j) in arcs if pulp.value(flow[f][(i, j)]) > 0]
    
    for arc in used_arcs:
        path_flow += pulp.value(flow[f][arc])
        path_cost += pulp.value(flow[f][arc]) * arc_data[arc]['C']
    
    route = [source[f]]
    current_node = source[f]
    while current_node != destination[f]:
        for arc in used_arcs:
            if arc[0] == current_node:
                route.append(arc[1])
                current_node = arc[1]
                break
                
    optimized_paths["paths"].append({
        "source": source[f],
        "destination": destination[f],
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

total_cost = pulp.value(problem.objective)

optimized_paths['total_cost'] = total_cost

import json
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')