import pulp

# Input data
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

# Define the problem
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

# Decision variables
# x_ij_k will represent the flow of data from node i to j for flow requirement k
flows = {}
for link_index in range(data['NumLinks']):
    i, j = data['StartNode'][link_index], data['EndNode'][link_index]
    for k in range(data['NumFlowReqs']):
        flows[(i, j, k)] = pulp.LpVariable(f"x_{i}_{j}_{k}", lowBound=0)

# Objective function
problem += pulp.lpSum(flows[(i, j, k)] * data['Cost'][link_index] 
                      for link_index in range(data['NumLinks']) 
                      for i, j in [(data['StartNode'][link_index], data['EndNode'][link_index])]
                      for k in range(data['NumFlowReqs']))

# Constraints

# Capacity constraints for each link
for link_index in range(data['NumLinks']):
    i, j = data['StartNode'][link_index], data['EndNode'][link_index]
    problem += pulp.lpSum(flows[(i, j, k)] for k in range(data['NumFlowReqs'])) <= data['Capacity'][link_index]

# Flow conservation constraints
# For each node and each flow requirement
nodes = set(data['StartNode']) | set(data['EndNode'])
for k in range(data['NumFlowReqs']):
    for node in nodes:
        flow_in = pulp.lpSum(flows[(i, node, k)] for i in nodes if (i, node, k) in flows)
        flow_out = pulp.lpSum(flows[(node, j, k)] for j in nodes if (node, j, k) in flows)

        if node == data['Source'][k]:
            problem += flow_out - flow_in == data['DataRate'][k]
        elif node == data['Destination'][k]:
            problem += flow_in - flow_out == data['DataRate'][k]
        else:
            problem += flow_in - flow_out == 0

# Solve the problem
problem.solve()

# Output results
output = {
    "optimized_paths": {
        "paths": [],
        "total_cost": None
    }
}

total_cost = 0
for k in range(data['NumFlowReqs']):
    path = {
        "source": data['Source'][k],
        "destination": data['Destination'][k],
        "route": [],
        "path_flow": 0,
        "path_cost": 0
    }
    for link_index in range(data['NumLinks']):
        i, j = data['StartNode'][link_index], data['EndNode'][link_index]
        flow_value = pulp.value(flows[(i, j, k)])
        if flow_value > 0:
            path["route"].extend([i, j])
            path["path_flow"] += flow_value
            path["path_cost"] += flow_value * data['Cost'][link_index]
    total_cost += path["path_cost"]
    output["optimized_paths"]["paths"].append(path)

output["optimized_paths"]["total_cost"] = total_cost

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')