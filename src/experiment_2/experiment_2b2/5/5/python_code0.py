import pulp

# Extract data from the input JSON format
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

# Initialize the optimization problem
problem = pulp.LpProblem("Minimize_Cost_Flow", pulp.LpMinimize)

# Extract relevant data
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Number of links and flow requests
num_links = data['NumLinks']
num_flow_reqs = data['NumFlowReqs']

# Variables to denote flow on each link for each data flow
flow_vars = {}
for r in range(num_flow_reqs):
    for l in range(num_links):
        flow_vars[(r, l)] = pulp.LpVariable(f'flow_{r}_{l}', 0, capacities[l], cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(r, l)] * costs[l] for r in range(num_flow_reqs) for l in range(num_links))

# Constraints to ensure data is routed correctly from source to destinations
for r in range(num_flow_reqs):
    # Flow conservation for each node
    for node in set(start_nodes + end_nodes):
        inflow = pulp.lpSum(flow_vars[(r, l)] for l in range(num_links) if end_nodes[l] == node)
        outflow = pulp.lpSum(flow_vars[(r, l)] for l in range(num_links) if start_nodes[l] == node)
        if node == sources[r]:
            # Source node
            problem += (outflow - inflow == data_rates[r])
        elif node == destinations[r]:
            # Destination node
            problem += (inflow - outflow == data_rates[r])
        else:
            # Intermediate nodes
            problem += (inflow - outflow == 0)

# Solve the problem
problem.solve()

# Collecting results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for r in range(num_flow_reqs):
    path = {"source": sources[r], "destination": destinations[r], "route": [sources[r]], "path_flow": 0, "path_cost": 0}
    for l in range(num_links):
        flow = flow_vars[(r, l)].varValue
        if flow > 0:
            path["route"].append(end_nodes[l])
            path["path_flow"] += flow
            path["path_cost"] += flow * costs[l]
    optimized_paths["paths"].append(path)

print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')