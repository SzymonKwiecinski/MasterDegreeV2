import pulp

# Load data from JSON
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
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

# Variables
flows = {}
for idx in range(data['NumLinks']):
    for flow in range(data['NumFlowReqs']):
        flows[(flow, data['StartNode'][idx], data['EndNode'][idx])] = pulp.LpVariable(
            f"flow_{flow}_{data['StartNode'][idx]}_{data['EndNode'][idx]}",
            lowBound=0,
            cat='Continuous'
        )

# Objective function
problem += pulp.lpSum([
    flows[(flow, data['StartNode'][idx], data['EndNode'][idx])] * data['Cost'][idx]
    for idx in range(data['NumLinks'])
    for flow in range(data['NumFlowReqs'])
])

# Constraints
# Capacity constraints
for idx in range(data['NumLinks']):
    problem += pulp.lpSum([
        flows[(flow, data['StartNode'][idx], data['EndNode'][idx])]
        for flow in range(data['NumFlowReqs'])
    ]) <= data['Capacity'][idx], f"Cap_{data['StartNode'][idx]}_{data['EndNode'][idx]}"

# Flow conservation constraints
nodes = set(data['StartNode']) | set(data['EndNode'])
for flow in range(data['NumFlowReqs']):
    source = data['Source'][flow]
    destination = data['Destination'][flow]
    for node in nodes:
        if node == source:
            problem += (pulp.lpSum([flows[(flow, node, j)] for j in nodes if (flow, node, j) in flows]) -
                        pulp.lpSum([flows[(flow, i, node)] for i in nodes if (flow, i, node) in flows]) ==
                        data['DataRate'][flow]), f"FlowConservation_Source_{flow}_{node}"
        elif node == destination:
            problem += (pulp.lpSum([flows[(flow, i, node)] for i in nodes if (flow, i, node) in flows]) -
                        pulp.lpSum([flows[(flow, node, j)] for j in nodes if (flow, node, j) in flows]) ==
                        data['DataRate'][flow]), f"FlowConservation_Destination_{flow}_{node}"
        else:
            problem += (pulp.lpSum([flows[(flow, node, j)] for j in nodes if (flow, node, j) in flows]) -
                        pulp.lpSum([flows[(flow, i, node)] for i in nodes if (flow, i, node) in flows]) ==
                        0), f"FlowConservation_{flow}_{node}"

# Solve the problem
problem.solve()

# Collect results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for flow in range(data['NumFlowReqs']):
    path_details = {
        "source": data['Source'][flow],
        "destination": data['Destination'][flow],
        "route": [],
        "path_flow": 0,
        "path_cost": 0
    }

    for idx in range(data['NumLinks']):
        if pulp.value(flows[(flow, data['StartNode'][idx], data['EndNode'][idx])]) > 0:
            path_details["route"].append((data['StartNode'][idx], data['EndNode'][idx]))
            flow_value = pulp.value(flows[(flow, data['StartNode'][idx], data['EndNode'][idx])])
            path_details["path_flow"] += flow_value
            path_details["path_cost"] += flow_value * data['Cost'][idx]

    optimized_paths["paths"].append(path_details)

print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')