import pulp
import json

# Load the data
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

# Unpack the data
links = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Initialize the problem
problem = pulp.LpProblem("NetworkFlowMinCost", pulp.LpMinimize)

# Variables
flow_vars = {}
for f in range(flow_reqs):
    for l in range(links):
        flow_vars[(f, l)] = pulp.LpVariable(f"Flow_{f}_{l}", 0, capacities[l])

# Objective Function: Minimize the total cost
problem += pulp.lpSum(flow_vars[(f, l)] * costs[l] for f in range(flow_reqs) for l in range(links))

# Constraints: 
# 1. Flow conservation: Ensure data flows from sources to destinations
for f in range(flow_reqs):
    for node in set(start_nodes + end_nodes):
        inflow = pulp.lpSum(flow_vars[(f, l)] for l in range(links) if end_nodes[l] == node)
        outflow = pulp.lpSum(flow_vars[(f, l)] for l in range(links) if start_nodes[l] == node)

        if node == sources[f]:
            problem += outflow - inflow == data_rates[f]
        elif node == destinations[f]:
            problem += inflow - outflow == data_rates[f]
        else:
            problem += inflow - outflow == 0

# Capacity constraints
for l in range(links):
    problem += pulp.lpSum(flow_vars[(f, l)] for f in range(flow_reqs)) <= capacities[l]

# Solve the problem
problem.solve()

# Collect the results
result = {
    "optimized_paths": {
        "paths": [],
        "total_cost": pulp.value(problem.objective)
    }
}

for f in range(flow_reqs):
    path_flow = []
    path_cost = 0
    route = [sources[f]]
    current_node = sources[f]
    while current_node != destinations[f]:
        for l in range(links):
            if start_nodes[l] == current_node and pulp.value(flow_vars[(f, l)]) > 0:
                route.append(end_nodes[l])
                path_flow.append(pulp.value(flow_vars[(f, l)]))
                path_cost += pulp.value(flow_vars[(f, l)]) * costs[l]
                current_node = end_nodes[l]
                break
    
    result["optimized_paths"]["paths"].append({
        "source": sources[f],
        "destination": destinations[f],
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output the result
output_json = json.dumps(result, indent=4)
print(output_json)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')